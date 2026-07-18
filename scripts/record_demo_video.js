const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const BASE_URL = process.env.DEMO_BASE_URL || "http://127.0.0.1:9011";
const OUTPUT_DIR = path.resolve(process.env.DEMO_OUTPUT_DIR || path.join("outputs", "demo-video"));
const VIDEO_BASENAME = process.env.DEMO_VIDEO_BASENAME || "ksp-catalyst-detailed-demo";

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function clickUnique(page, selector, label) {
  if (selector !== "#tourModalAcknowledgeBtn") {
    await dismissTourIfPresent(page);
  }
  const locator = page.locator(selector);
  const count = await locator.count();
  if (count !== 1) {
    throw new Error(`${label || selector} resolved to ${count} elements`);
  }
  await locator.click();
}

async function fillUnique(page, selector, value, label) {
  const locator = page.locator(selector);
  const count = await locator.count();
  if (count !== 1) {
    throw new Error(`${label || selector} resolved to ${count} elements`);
  }
  await locator.fill(value);
}

async function showCaption(page, text) {
  await page.evaluate((caption) => {
    document.getElementById("tourModalOverlay")?.classList.add("is-hidden");
    let node = document.getElementById("demoVideoCaption");
    if (!node) {
      node = document.createElement("div");
      node.id = "demoVideoCaption";
      node.style.position = "fixed";
      node.style.left = "24px";
      node.style.bottom = "24px";
      node.style.maxWidth = "520px";
      node.style.padding = "14px 18px";
      node.style.border = "1px solid rgba(255,255,255,0.24)";
      node.style.borderRadius = "8px";
      node.style.background = "rgba(2,15,31,0.88)";
      node.style.color = "#fff";
      node.style.font = "600 16px/1.45 Arial, sans-serif";
      node.style.boxShadow = "0 18px 48px rgba(0,0,0,0.35)";
      node.style.zIndex = "2147483647";
      node.style.pointerEvents = "none";
      document.body.appendChild(node);
    }
    node.textContent = caption;
  }, text);
  await delay(Number(process.env.DEMO_CAPTION_DELAY_MS || 1900));
}

async function waitForVisible(page, selector, label) {
  await page.locator(selector).waitFor({ state: "visible", timeout: 30000 });
  if (label) {
    await showCaption(page, label);
  }
}

async function dismissTourIfPresent(page) {
  const overlay = page.locator("#tourModalOverlay:not(.is-hidden)");
  if ((await overlay.count()) === 1 && (await overlay.isVisible())) {
    const button = page.locator("#tourModalAcknowledgeBtn");
    if ((await button.count()) === 1 && (await button.isVisible())) {
      await clickUnique(page, "#tourModalAcknowledgeBtn", "tour acknowledge");
      await page.locator("#tourModalOverlay.is-hidden").waitFor({ state: "attached", timeout: 10000 });
    } else {
      await page.evaluate(() => document.getElementById("tourModalOverlay")?.classList.add("is-hidden"));
    }
  }
}

async function openPanel(page, panel, caption) {
  await dismissTourIfPresent(page);
  const clicked = await page.evaluate((targetPanel) => {
    const selector = `.sidebar .nav-item[data-panel="${targetPanel}"], .bottom-nav-item[data-panel="${targetPanel}"], [data-panel-jump="${targetPanel}"]`;
    const candidates = Array.from(document.querySelectorAll(selector));
    const visible = candidates.find((node) => {
      const rect = node.getBoundingClientRect();
      const style = window.getComputedStyle(node);
      return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
    });
    if (visible) {
      visible.click();
      return true;
    }
    return false;
  }, panel);
  if (!clicked) {
    await page.evaluate((targetPanel) => {
      try {
        if (typeof window.setPanel === "function") {
          window.setPanel(targetPanel);
          return;
        }
      } catch (_error) {
        // Fall through to a display-only panel switch so the recording can continue.
      }
      const shell = document.getElementById("shell");
      if (shell) shell.setAttribute("data-active-panel", targetPanel);
      document.querySelectorAll(".panel").forEach((panelNode) => {
        panelNode.classList.toggle("is-active", panelNode.id === targetPanel);
      });
    }, panel);
  }
  await page.locator(`#${panel}.panel.is-active`).waitFor({ state: "visible", timeout: 30000 });
  await delay(700);
  await dismissTourIfPresent(page);
  if (caption) await showCaption(page, caption);
}

async function submitChatQuery(page, query, caption) {
  await openPanel(page, "command");
  const previousAnswers = await page.locator(".message.assistant-message, .assistant-answer").count();
  await fillUnique(page, "#queryInput", query, "AI query input");
  await showCaption(page, `Chatbot query: ${query}`);
  await clickUnique(page, "#queryForm button[type='submit']", "send AI query");
  await page.waitForFunction(
    (count) => document.querySelectorAll(".message.assistant-message, .assistant-answer").length > count,
    previousAnswers,
    { timeout: 45000 },
  );
  await delay(2200);
  if (caption) await showCaption(page, caption);
}

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: OUTPUT_DIR, size: { width: 1440, height: 900 } },
  });
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  await page.addInitScript(() => {
    localStorage.setItem("ksp_tour_date", new Date().toDateString());
    localStorage.setItem(
      "ksp_seen_tours",
      JSON.stringify([
        "command",
        "framework",
        "cases",
        "network",
        "patterns",
        "analytics",
        "profiling",
        "support",
        "overview",
        "map",
        "financial",
        "audit",
        "admin",
        "biometric",
        "log_crime",
      ]),
    );
  });

  await page.goto(BASE_URL, { waitUntil: "domcontentloaded" });
  await waitForVisible(page, "[data-view='login']", "KSP AI opens with a secure role-based login.");
  await clickUnique(page, ".evaluator-login-btn[data-username='superadmin']", "superadmin evaluator login");
  await page.locator("[data-view='shell']:not(.is-hidden)").waitFor({ state: "visible", timeout: 30000 });
  await page.waitForFunction(() => document.getElementById("apiStatus")?.textContent?.includes("online"));
  await showCaption(page, "Super Admin enters the live command center with seeded demo/template FIR data.");
  await dismissTourIfPresent(page);

  await showCaption(page, "Part 1: five detailed chatbot queries against the seeded Catalyst demo database.");
  await submitChatQuery(
    page,
    "Show FIR details for BLR-CYB-042",
    "Query 1 returns a specific FIR summary, status, district, suspect, and evidence references.",
  );
  await submitChatQuery(
    page,
    "Create suspect profile for Pooja Naik",
    "Query 2 builds a criminology-style suspect profile using only accessible case records.",
  );
  await submitChatQuery(
    page,
    "Show criminal network for Pooja Naik",
    "Query 3 routes to network intelligence and links the suspect to FIRs, locations, and related entities.",
  );
  await submitChatQuery(
    page,
    "Show money trail for Pooja Naik",
    "Query 4 traces high-value transfers, mule accounts, bank branches, and linked FIRs.",
  );
  await submitChatQuery(
    page,
    "Forecast crime hotspot risk for the next 7 days",
    "Query 5 switches to proactive forecasting and hotspot-risk intelligence.",
  );

  await showCaption(page, "Part 2: dashboard walkthrough of the operational modules.");

  await openPanel(page, "framework", "Framework shows the required solution pillars and module coverage for the hackathon brief.");
  await delay(1800);

  await openPanel(page, "cases", "Case registry lists authorized FIR records with district, status, suspect, and sensitivity controls.");
  await fillUnique(page, "#caseSearchInput", "Pooja Naik", "case search");
  await delay(1600);
  await showCaption(page, "Hash-prefix case search filters records by suspect, FIR, district, or source ID.");

  await openPanel(page, "map", "GIS mapping plots official coordinates and local heat signals across Karnataka districts.");
  await clickUnique(page, "#heatToggleBtn", "toggle heat layer");
  await delay(1200);
  await clickUnique(page, "#localMapBtn", "local map mode");
  await delay(1200);

  await openPanel(page, "network", "Criminal network analysis links FIRs, suspects, accounts, banks, IFSCs, branches, and transfer edges.");
  await fillUnique(page, "#networkFocusInput", "IN-BLR-MULE-1001", "network focus");
  await page.locator("#networkFocusType").selectOption("account");
  await clickUnique(page, "#networkFocusApply", "network focus run");
  await delay(1800);
  await showCaption(page, "Focused network search pivots from a mule account to linked cases and transaction trails.");
  await clickUnique(page, "[data-network-mode='money']", "money flow mode");
  await delay(1600);
  await showCaption(page, "Money-flow mode highlights financial accounts and transfer relationships.");

  await openPanel(page, "patterns", "Pattern discovery shows crime clusters, modus operandi groups, seasonal signals, and data-quality checks.");
  await delay(2200);

  await openPanel(page, "analytics", "Sociological analytics explains district trends with demographic and community indicators.");
  await delay(2200);

  await openPanel(page, "profiling", "Offender profiling lets investigators search a named suspect and review behavioral indicators.");
  await fillUnique(page, "#suspectInput", "Pooja Naik", "suspect profile input");
  await clickUnique(page, "#profileBtn", "profile search");
  await delay(2200);

  await openPanel(page, "support", "Investigator decision support creates a case intelligence pack and evidence trail.");
  await page.locator("#caseSelect").selectOption({ index: 0 });
  await clickUnique(page, "#supportBtn", "build support pack");
  await delay(2200);
  await clickUnique(page, "#explainBtn", "generate evidence trail");
  await delay(2200);

  await openPanel(page, "overview", "Forecasting overview summarizes live posture, open FIRs, hotspots, and early warnings.");
  await delay(2200);

  await openPanel(page, "financial", "Financial intelligence flags high-value transfers, structuring signals, account links, and risk findings.");
  await delay(2400);

  await openPanel(page, "audit", "Explainable AI and audit verifies the cryptographic hash chain and recent governed actions.");
  await clickUnique(page, "#auditRefresh", "refresh audit");
  await delay(2200);

  await openPanel(page, "admin", "Admin governance shows role-based access, active users, password reset controls, and rate-limit alerts.");
  await clickUnique(page, "#refreshUsers", "refresh users");
  await delay(2200);

  await openPanel(page, "biometric", "Biometric settings explain WebAuthn fingerprint/passkey registration without storing raw fingerprints.");
  await delay(2000);

  await openPanel(page, "log_crime", "Crime logging captures accused details, witnesses, counsel, bail information, and BNS charge sections.");
  await clickUnique(page, "#autoFillCrimeLogBtn", "auto fill crime log");
  await page.locator("#crimeLogStatus.success").waitFor({ state: "visible", timeout: 30000 });
  await showCaption(page, "Crime logging writes a governed record and returns a visible success state.");

  await openPanel(page, "command", "Demo complete: Catalyst AppSail hosts one secure app for chatbot intelligence, dashboards, audit, admin, and logging.");
  await delay(2000);

  await context.close();
  await browser.close();
  const videos = fs
    .readdirSync(OUTPUT_DIR)
    .filter((name) => name.endsWith(".webm"))
    .map((name) => path.join(OUTPUT_DIR, name))
    .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
  if (!videos.length) {
    throw new Error("Playwright did not create a video file");
  }
  const finalPath = path.join(OUTPUT_DIR, `${VIDEO_BASENAME}.webm`);
  fs.copyFileSync(videos[0], finalPath);
  console.log(finalPath);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
