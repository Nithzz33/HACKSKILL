const storedMapProvider = localStorage.getItem("kspMapProvider");
const storedLanguage = localStorage.getItem("kspUiLanguage");
const storedTheme = localStorage.getItem("kspTheme");
const KARNATAKA_CENTER = [14.52, 75.72];
const PROFILE_PHOTOS = [
  "/static/assets/profiles/person-01.jpg",
  "/static/assets/profiles/person-02.png",
  "/static/assets/profiles/person-03.png",
  "/static/assets/profiles/person-04.png",
  "/static/assets/profiles/person-05.png",
  "/static/assets/profiles/person-06.jpeg",
  "/static/assets/profiles/person-07.jpeg",
  "/static/assets/profiles/person-08.jpeg",
  "/static/assets/profiles/person-09.jpeg",
  "/static/assets/profiles/person-10.jpg",
];
const PANEL_KEYS = {
  admin: "Administration",
  analytics: "Analytics",
  audit: "Audit",
  biometric: "Settings",
  cases: "Cases",
  command: "AI Assistant",
  financial: "Financial Intelligence",
  framework: "AI Assistant",
  map: "Geospatial Intelligence",
  network: "Networks",
  overview: "Home",
  patterns: "Pattern Analysis",
  sna: "snaDashboard",
  support: "Investigations",
};
const I18N = {
  en: {
    accessibleNetwork: "Accessible case network",
    accountLinks: "Account links",
    analytics: "Analytics",
    analyst: "Analyst",
    apiCheck: "API check",
    apiOffline: "API offline",
    apiOnline: "API online",
    appTitle: "Karnataka State Police Intelligent Systems",
    ask: "Ask",
    askAi: "Ask AI",
    audit: "Audit",
    auditHashChain: "Audit hash chain",
    auditLog: "Audit log",
    authorizedRecords: "Authorized records",
    authorizedUser: "Authorized user",
    bank: "Bank",
    bankManager: "Bank manager",
    biometric: "Biometric",
    byline: "By Jaswinzz Gowda",
    buildSupportPack: "Build support pack",
    branch: "Branch",
    caseMix: "Case mix",
    caseRegistry: "Case registry",
    fileLookup: "File lookup",
    fileLookupPlaceholder: "Search file, FIR, district, person, hash...",
    filePreview: "File preview",
    filePreviewFailed: "File preview failed.",
    filePreviewUnavailable: "This file type cannot be rendered inline yet. Upload or preview a PDF/image/text file for browser pages.",
    linkedFilePages: "Linked FIR/case file pages",
    caseSearchPlaceholder: "Search FIR, district, person, status, source ID...",
    cases: "Cases",
    checking: "Checking",
    clustersAndMo: "Clusters and modus operandi",
    collapseSidebar: "Collapse sidebar",
    command: "Command",
    conversationalIntelligence: "Conversational intelligence",
    createAccount: "Create account",
    createUser: "Create user",
    crimeHeatMap: "Crime heat map and patrol view",
    dataQuality: "Data quality",
    decisionSupport: "Decision support",
    deadEnd: "Dead end",
    district: "District",
    districtCommandMap: "Karnataka District Command Map",
    districtOrState: "District or state",
    districtPlanning: "District planning",
    districtRosterCount: "31 district roster",
    districts: "Districts",
    evidenceCommand: "Evidence-bound command",
    evidenceTrail: "Evidence trail",
    explainSelectedCase: "Explain selected case",
    explainability: "Explainability",
    exportPdf: "Export PDF",
    financial: "Financial",
    financialAccount: "Financial account",
    financialAnalysis: "Financial analysis",
    fingerprintCancelled: "Fingerprint action was cancelled.",
    fingerprintHelp: "Use Windows Hello, passkey, or a WebAuthn-compatible fingerprint scanner. Raw fingerprint images never leave the device.",
    fingerprintLogin: "Fingerprint login",
    fingerprintModule: "Fingerprint module",
    fingerprintPrompt: "Touch your fingerprint device or approve Windows Hello.",
    fingerprintRegistered: "Fingerprint device registered.",
    fingerprintSecurity: "Fingerprint security",
    fingerprintUnsupported: "Fingerprint login is not available in this browser/device.",
    fingerprintUsernameRequired: "Enter username before fingerprint login.",
    findings: "Findings",
    fir: "FIR",
    forecast: "Forecast",
    forecastHotspots: "Forecast hotspots",
    framework: "Framework",
    fullName: "Full name",
    geospatialIntelligence: "Geospatial intelligence",
    googleKeyPlaceholder: "Optional Google Maps JavaScript API key",
    googleMaps: "Google Maps",
    heatMap: "Heat map",
    ifsc: "IFSC",
    implementedSurface: "Implemented system surface",
    integrity: "Integrity",
    intelligentSystems: "Intelligent Systems",
    investigator: "Investigator",
    ksp: "Karnataka State Police",
    language: "Language",
    launchQuery: "Launch query",
    leafletMap: "Leaflet map",
    liveAdminAlerts: "Live admin alerts",
    livePosture: "Live operational posture",
    logout: "Logout",
    map: "Map",
    mapNote: "Google Maps mode loads Google map tiles in your browser. The heat layer is rendered locally from authorized case data.",
    moduleCoverage: "Module coverage",
    namedSuspectProfile: "Named suspect profile",
    network: "Network",
    newConversation: "New conversation",
    observation: "Observation",
    officialCoordinates: "Official coordinates",
    officialFieldCoverage: "Official field coverage",
    openSidebar: "Open sidebar",
    operationalDashboard: "Operational dashboard",
    overview: "Overview",
    password: "Password",
    patternDiscovery: "Pattern discovery",
    patterns: "Patterns",
    policymaker: "Policymaker",
    profiles: "Profiles",
    previewCaseFiles: "Preview uploaded FIR and case files",
    previewFile: "Preview file",
    queryPlaceholder: "Ask about cases, trends, suspects, districts, or next steps",
    rateLimitBreaches: "Rate limit breaches",
    recentEvents: "Recent events",
    refreshAudit: "Refresh audit",
    refreshCases: "Refresh cases",
    refreshRateAlerts: "Refresh rate limit alerts",
    refreshUsers: "Refresh users",
    relationshipGraph: "Relationship graph",
    restricted: "Restricted",
    selectedCase: "Selected case",
    selectFileToPreview: "Select an uploaded file to preview pages.",
    noFileSelected: "No file selected",
    noUploadedFiles: "No uploaded files match this lookup.",
    sensitivity: "Sensitivity",
    setupNote: "Use an authorized account provisioned by your administrator.",
    signIn: "Sign in",
    sociological: "Sociological",
    spatialTriage: "Spatial triage",
    standard: "Standard",
    status: "Status",
    superAdmin: "Super Admin",
    supervisor: "Supervisor",
    support: "Support",
    suspect: "Suspect",
    suspectPlaceholder: "Enter suspect/person name from official records",
    temporaryPassword: "Temporary password",
    topView: "Top view",
    transactionTriage: "Transaction triage",
    translate: "Translate",
    translationAdapter: "Translation adapter",
    trends: "Trends",
    triage: "Triage",
    typeAndEvents: "Type, month, and events",
    toggleHeatLayer: "Toggle heat layer",
    useKey: "Use key",
    userAccessControl: "User access control",
    username: "Username",
    viewer: "Viewer",
    voiceAsk: "Voice ask",
    workloadInsights: "Workload insights",
    zonesAndIncidents: "Zones and incidents",
  },
  kn: {
    accessibleNetwork: "ಪ್ರವೇಶಯೋಗ್ಯ ಪ್ರಕರಣ ಜಾಲ",
    accountLinks: "ಖಾತೆ ಸಂಪರ್ಕಗಳು",
    analytics: "ವಿಶ್ಲೇಷಣೆ",
    analyst: "ವಿಶ್ಲೇಷಕ",
    apiCheck: "ಎಪಿಐ ಪರಿಶೀಲನೆ",
    apiOffline: "ಎಪಿಐ ಆಫ್‌ಲೈನ್",
    apiOnline: "ಎಪಿಐ ಆನ್‌ಲೈನ್",
    appTitle: "ಕರ್ನಾಟಕ ರಾಜ್ಯ ಪೊಲೀಸ್ ಇಂಟೆಲಿಜೆಂಟ್ ಸಿಸ್ಟಮ್ಸ್",
    ask: "ಕೇಳಿ",
    askAi: "ಎಐ ಕೇಳಿ",
    audit: "ಆಡಿಟ್",
    auditHashChain: "ಆಡಿಟ್ ಹ್ಯಾಶ್ ಸರಣಿ",
    auditLog: "ಆಡಿಟ್ ದಾಖಲೆ",
    authorizedRecords: "ಅಧಿಕೃತ ದಾಖಲೆಗಳು",
    authorizedUser: "ಅಧಿಕೃತ ಬಳಕೆದಾರ",
    byline: "ಜಸ್ವಿನ್ಜ್ ಗೌಡ ಅವರಿಂದ",
    buildSupportPack: "ಬೆಂಬಲ ಪ್ಯಾಕ್ ರಚಿಸಿ",
    caseMix: "ಪ್ರಕರಣ ಮಿಶ್ರಣ",
    caseRegistry: "ಪ್ರಕರಣ ನೋಂದಣಿ",
    caseSearchPlaceholder: "ಎಫ್ಐಆರ್, ಜಿಲ್ಲೆ, ವ್ಯಕ್ತಿ, ಸ್ಥಿತಿ, ಮೂಲ ಐಡಿ ಹುಡುಕಿ...",
    cases: "ಪ್ರಕರಣಗಳು",
    checking: "ಪರಿಶೀಲನೆ",
    clustersAndMo: "ಕ್ಲಸ್ಟರ್ ಮತ್ತು ಕಾರ್ಯ ವಿಧಾನ",
    collapseSidebar: "ಬದಿಪಟ್ಟಿ ಕುಗ್ಗಿಸಿ",
    command: "ಕಮಾಂಡ್",
    conversationalIntelligence: "ಸಂಭಾಷಣಾತ್ಮಕ ಗುಪ್ತಚರ",
    createAccount: "ಖಾತೆ ರಚನೆ",
    createUser: "ಬಳಕೆದಾರ ರಚಿಸಿ",
    crimeHeatMap: "ಅಪರಾಧ ಹೀಟ್ ಮ್ಯಾಪ್ ಮತ್ತು ಪೆಟ್ರೋಲ್ ನೋಟ",
    dataQuality: "ಡೇಟಾ ಗುಣಮಟ್ಟ",
    decisionSupport: "ನಿರ್ಧಾರ ಬೆಂಬಲ",
    district: "ಜಿಲ್ಲೆ",
    districtCommandMap: "ಕರ್ನಾಟಕ ಜಿಲ್ಲಾ ಕಮಾಂಡ್ ನಕ್ಷೆ",
    districtOrState: "ಜಿಲ್ಲೆ ಅಥವಾ ರಾಜ್ಯ",
    districtPlanning: "ಜಿಲ್ಲಾ ಯೋಜನೆ",
    districtRosterCount: "31 ಜಿಲ್ಲೆಗಳ ಪಟ್ಟಿ",
    districts: "ಜಿಲ್ಲೆಗಳು",
    evidenceCommand: "ಸಾಕ್ಷ್ಯಾಧಾರಿತ ಕಮಾಂಡ್",
    evidenceTrail: "ಸಾಕ್ಷ್ಯ ಹಾದಿ",
    explainSelectedCase: "ಆಯ್ದ ಪ್ರಕರಣ ವಿವರಿಸಿ",
    explainability: "ವಿವರಣಾತ್ಮಕತೆ",
    exportPdf: "ಪಿಡಿಎಫ್ ರಫ್ತು",
    financial: "ಹಣಕಾಸು",
    financialAnalysis: "ಹಣಕಾಸು ವಿಶ್ಲೇಷಣೆ",
    findings: "ಸೂಚನೆಗಳು",
    fir: "ಎಫ್ಐಆರ್",
    forecast: "ಮುನ್ಸೂಚನೆ",
    forecastHotspots: "ಹಾಟ್‌ಸ್ಪಾಟ್ ಮುನ್ಸೂಚನೆ",
    fullName: "ಪೂರ್ಣ ಹೆಸರು",
    geospatialIntelligence: "ಭೌಗೋಳಿಕ ಗುಪ್ತಚರ",
    googleKeyPlaceholder: "ಐಚ್ಛಿಕ Google Maps JavaScript API ಕೀ",
    googleMaps: "Google Maps",
    heatMap: "ಹೀಟ್ ಮ್ಯಾಪ್",
    implementedSurface: "ಅಮಲಾದ ವ್ಯವಸ್ಥಾ ವ್ಯಾಪ್ತಿ",
    integrity: "ಅಖಂಡತೆ",
    intelligentSystems: "ಇಂಟೆಲಿಜೆಂಟ್ ಸಿಸ್ಟಮ್ಸ್",
    investigator: "ತನಿಖಾಧಿಕಾರಿ",
    ksp: "ಕರ್ನಾಟಕ ರಾಜ್ಯ ಪೊಲೀಸ್",
    language: "ಭಾಷೆ",
    leafletMap: "Leaflet ನಕ್ಷೆ",
    liveAdminAlerts: "ಲೈವ್ ನಿರ್ವಾಹಕ ಎಚ್ಚರಿಕೆಗಳು",
    livePosture: "ಲೈವ್ ಕಾರ್ಯಾಚರಣಾ ಸ್ಥಿತಿ",
    logout: "ಲಾಗ್ ಔಟ್",
    map: "ನಕ್ಷೆ",
    mapNote: "Google Maps ಮೋಡ್ ಬ್ರೌಸರ್‌ನಲ್ಲಿ Google ನಕ್ಷೆ ಟೈಲ್‌ಗಳನ್ನು ಲೋಡ್ ಮಾಡುತ್ತದೆ. ಹೀಟ್ ಲೇಯರ್ ಅಧಿಕೃತ ಪ್ರಕರಣ ಡೇಟಾದಿಂದ ಸ್ಥಳೀಯವಾಗಿ ರೆಂಡರ್ ಆಗುತ್ತದೆ.",
    moduleCoverage: "ಮಾಡ್ಯೂಲ್ ವ್ಯಾಪ್ತಿ",
    namedSuspectProfile: "ಹೆಸರಿತ ಆರೋಪಿ ಪ್ರೊಫೈಲ್",
    network: "ಜಾಲ",
    newConversation: "ಹೊಸ ಸಂಭಾಷಣೆ",
    observation: "ಪರಿವೀಕ್ಷಣೆ",
    officialCoordinates: "ಅಧಿಕೃತ ಸ್ಥಳಾಂಕಗಳು",
    officialFieldCoverage: "ಅಧಿಕೃತ ಕ್ಷೇತ್ರ ವ್ಯಾಪ್ತಿ",
    openSidebar: "ಬದಿಪಟ್ಟಿ ತೆರೆಯಿರಿ",
    operationalDashboard: "ಕಾರ್ಯಾಚರಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
    overview: "ಸಾರಾಂಶ",
    password: "ಪಾಸ್‌ವರ್ಡ್",
    patternDiscovery: "ಮಾದರಿ ಪತ್ತೆ",
    patterns: "ಮಾದರಿಗಳು",
    policymaker: "ನೀತಿನಿರ್ಮಾಪಕ",
    profiles: "ಪ್ರೊಫೈಲ್‌ಗಳು",
    queryPlaceholder: "ಪ್ರಕರಣಗಳು, ಪ್ರವೃತ್ತಿಗಳು, ಆರೋಪಿಗಳು, ಜಿಲ್ಲೆಗಳು ಅಥವಾ ಮುಂದಿನ ಕ್ರಮಗಳ ಬಗ್ಗೆ ಕೇಳಿ",
    rateLimitBreaches: "ದರ ಮಿತಿ ಉಲ್ಲಂಘನೆಗಳು",
    recentEvents: "ಇತ್ತೀಚಿನ ಘಟನೆಗಳು",
    refreshAudit: "ಆಡಿಟ್ ಮರುಲೋಡ್",
    refreshCases: "ಪ್ರಕರಣಗಳನ್ನು ಮರುಲೋಡ್",
    refreshRateAlerts: "ದರ ಮಿತಿ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಮರುಲೋಡ್",
    refreshUsers: "ಬಳಕೆದಾರರನ್ನು ಮರುಲೋಡ್",
    relationshipGraph: "ಸಂಬಂಧ ಗ್ರಾಫ್",
    restricted: "ನಿರ್ಬಂಧಿತ",
    selectedCase: "ಆಯ್ದ ಪ್ರಕರಣ",
    sensitivity: "ಸಂವೇದನಾಶೀಲತೆ",
    setupNote: "ನಿರ್ವಾಹಕರು ಒದಗಿಸಿದ ಅಧಿಕೃತ ಖಾತೆಯನ್ನು ಬಳಸಿ.",
    signIn: "ಸೈನ್ ಇನ್",
    sociological: "ಸಮಾಜಶಾಸ್ತ್ರೀಯ",
    spatialTriage: "ಸ್ಥಳೀಯ ಟ್ರಿಯಾಜ್",
    standard: "ಸಾಮಾನ್ಯ",
    status: "ಸ್ಥಿತಿ",
    superAdmin: "ಸೂಪರ್ ನಿರ್ವಾಹಕ",
    supervisor: "ಮೇಲ್ವಿಚಾರಕ",
    support: "ಬೆಂಬಲ",
    suspect: "ಆರೋಪಿ",
    suspectPlaceholder: "ಅಧಿಕೃತ ದಾಖಲೆಗಳಲ್ಲಿ ಇರುವ ಆರೋಪಿ/ವ್ಯಕ್ತಿಯ ಹೆಸರು ನಮೂದಿಸಿ",
    temporaryPassword: "ತಾತ್ಕಾಲಿಕ ಪಾಸ್‌ವರ್ಡ್",
    topView: "ಮೇಲ್ದೃಶ್ಯ",
    transactionTriage: "ವಹಿವಾಟು ಟ್ರಿಯಾಜ್",
    translate: "ಅನುವಾದ",
    translationAdapter: "ಅನುವಾದ ಅಡಾಪ್ಟರ್",
    trends: "ಪ್ರವೃತ್ತಿಗಳು",
    triage: "ಟ್ರಿಯಾಜ್",
    typeAndEvents: "ಪ್ರಕಾರ, ತಿಂಗಳು ಮತ್ತು ಘಟನೆಗಳು",
    toggleHeatLayer: "ಹೀಟ್ ಲೇಯರ್ ಬದಲಿಸಿ",
    useKey: "ಕೀ ಬಳಸಿ",
    userAccessControl: "ಬಳಕೆದಾರ ಪ್ರವೇಶ ನಿಯಂತ್ರಣ",
    username: "ಬಳಕೆದಾರ ಹೆಸರು",
    viewer: "ವೀಕ್ಷಕ",
    voiceAsk: "ಧ್ವನಿ ಕೇಳಿ",
    workloadInsights: "ಕಾರ್ಯಭಾರ ಒಳನೋಟಗಳು",
    zonesAndIncidents: "ವಲಯಗಳು ಮತ್ತು ಘಟನೆಗಳು",
  },
};

Object.assign(I18N.en, {
  accessibleFlow: "Accessible flow",
  active: "Active",
  autoImportRows: "Auto-import rows",
  caseType: "Crime type",
  caseFileUpload: "Case file upload",
  caseSheet: "Case sheet",
  chainFailed: "Chain failed",
  chainValid: "Chain valid",
  checkedAuditEvents: "Checked audit events",
  chooseFileFirst: "Choose a file first.",
  closed: "Closed",
  conversationOpened: "Conversation opened. Ask for a case summary, district trend, suspect profile, pattern, financial trail, or next step.",
  correlation: "Correlation",
  correlations: "Correlations",
  crimeIntelligencePlatform: "Intelligent Conversational AI and Crime Analytics Platform",
  criminalNetworkDashboard: "Criminal Network Analysis dashboard",
  currentCases: "current case(s)",
  currentWorkload: "Current workload",
  edgeCsv: "Edge CSV",
  earlyWarning: "Early warning",
  earlyWarnings: "Early warnings",
  event: "Event",
  expectedSolution: "Expected solution framework",
  evidenceHash: "Evidence hash",
  fieldCoverageGood: "Official analytical fields are populated for the records in scope.",
  firCopy: "FIR copy",
  forecastPending: "Forecast data will appear after sign in.",
  high: "High",
  highValueTransfer: "High-value transfer",
  implemented: "Implemented",
  investigativeLeads: "Investigative leads",
  investigationTimeline: "Investigation timeline",
  low: "Low",
  medium: "Medium",
  moduleAdmin: "Super Admin User Management",
  moduleAdvanced: "Advanced Crime ML, Heatmap, Risk, and Anomaly Intelligence",
  moduleChat: "Conversational Crime Intelligence Interface",
  moduleDecision: "Decision Support",
  moduleExplain: "Explainable AI and Evidence Trails",
  moduleFinancial: "Financial Analysis",
  moduleForecast: "Forecasting and Early Warning",
  moduleGeo: "Leaflet Geographic Crime Map and Heat Layer",
  moduleGovernance: "RBAC, Data Masking, Rate Limiting, Session Revocation, Audit Logs",
  moduleLanguage: "Multi-lingual, Voice-ready, PDF Conversation Support",
  moduleNetwork: "Criminal Network and Relationship Analysis",
  modulePatterns: "Crime Pattern Discovery",
  moduleProfile: "Offender Profiling",
  moduleSearch: "Hash-Prefix Case Typeahead Search",
  moduleSocio: "Sociological Insights",
  moduleTrends: "Trend Analytics and Hotspots",
  nodeCsv: "Node CSV",
  openFullDashboard: "Open full dashboard",
  pngExport: "PNG export",
  professionalSna: "Professional SNA dashboard",
  solutionCoverage: "Solution coverage",
  snaDashboard: "SNA Dashboard",
  anomaly: "Anomaly",
  integratedDataset: "Integrated dataset",
  mlIncidents: "Imported incidents",
  riskAreas: "Risk areas",
  month: "Month",
  nextSteps: "Next steps",
  noCasesForRole: "No cases available for this role.",
  noClusters: "No repeat clusters",
  noClustersBody: "No repeated district, type, or modus operandi cluster is visible in authorized records.",
  noFinancialFindings: "No triage findings for accessible transactions.",
  noFindings: "No findings",
  noFingerprintStorage: "No fingerprint storage",
  noFingerprintStorageBody: "The system stores only a public credential key and sign counter; fingerprint templates remain protected by the device/OS.",
  registerFingerprint: "Register fingerprint device",
  webauthnOnly: "WebAuthn secure mode",
  webauthnOnlyBody: "Works with browser-supported biometric authenticators. Vendor-only USB scanners require their local SDK gateway before the browser can use them.",
  noLinkedCase: "No linked case",
  noPatternBars: "Official type, MO, month, or event fields are not populated yet.",
  none: "None",
  open: "Open",
  openCases: "Open cases",
  pending: "Pending",
  possibleCircularFlow: "Possible circular flow",
  possibleStructuring: "Possible structuring",
  projectedPlanning: "projected for planning",
  reasoningPath: "Reasoning path",
  riskScore: "Risk score",
  similarCases: "Similar cases",
  socialIndicator: "Social indicator",
  suspectAge: "Suspect age",
  suspectGender: "Suspect gender",
  totalAmount: "Total amount",
  transactions: "Transactions",
  triageSignals: "Triage signals",
  unavailable: "Unavailable",
  underReview: "Under review",
  uploadFile: "Upload file",
  uploadFirOrSheet: "Upload FIR copy or case sheet",
  uploading: "Uploading...",
  victimAge: "Victim age",
  victimGender: "Victim gender",
  visibleFinancialRecords: "Visible financial records",
  voiceFailed: "Voice capture failed.",
  voiceUnsupported: "Voice input is not available in this browser.",
});

Object.assign(I18N.en, {
  analyzingCrimeData: "Reading the crime records and preparing an answer...",
  answerSupport: "Answer support",
  crimeDataOnly: "Crime-data only",
  crimeRecordsOnly: "Uses crime records only",
  dataScope: "Data scope",
  evidenceAvailable: "Evidence available",
  evidenceCommand: "KSP AI crime assistant",
  evidenceMode: "Evidence mode",
  evidenceSources: "Evidence sources",
  filters: "Filters",
  importedAggregate: "Imported incident aggregate",
  localSearchIndex: "Local case search index",
  normalized: "Normalized",
  noExternalFacts: "Evidence trail available",
  noIndividualSources: "Aggregate-only response. Individual source rows are not exposed for this query.",
  nlpCleanup: "Understands normal questions",
  oneRecordFound: "1 visible case",
  oneSourceRecord: "1 source record",
  orchestrationFlow: "Orchestration flow",
  queryInterpretation: "Query interpretation",
  queryPlaceholder: "Ask like normal: show Karnataka cases, find Ravi Kumar, theft hotspots in Bengaluru, money trail for A1...",
  recordsMatched: "Visible cases",
  recordsFound: "visible cases",
  safeguards: "Safeguards",
  sourceRecordsLower: "source records",
  sourceRecords: "Source records",
  strictCrimeOnly: "Answers from crime records",
  selectedModule: "Selected module",
  terms: "Terms",
  unknown: "Unknown",
  viewEvidenceTrail: "Evidence and query reading",
});

Object.assign(I18N.kn, {
  accessibleFlow: "ಪ್ರವೇಶಯೋಗ್ಯ ಹರಿವು",
  active: "ಸಕ್ರಿಯ",
  caseType: "ಅಪರಾಧ ಪ್ರಕಾರ",
  chainFailed: "ಸರಣಿ ವಿಫಲವಾಗಿದೆ",
  chainValid: "ಸರಣಿ ಮಾನ್ಯವಾಗಿದೆ",
  checkedAuditEvents: "ಪರಿಶೀಲಿಸಿದ ಆಡಿಟ್ ಘಟನೆಗಳು",
  closed: "ಮುಚ್ಚಿದ",
  conversationOpened: "ಸಂಭಾಷಣೆ ತೆರೆಯಲಾಗಿದೆ. ಪ್ರಕರಣ ಸಾರಾಂಶ, ಜಿಲ್ಲಾ ಪ್ರವೃತ್ತಿ, ಆರೋಪಿ ಪ್ರೊಫೈಲ್, ಮಾದರಿ, ಹಣಕಾಸು ಹಾದಿ ಅಥವಾ ಮುಂದಿನ ಕ್ರಮವನ್ನು ಕೇಳಿ.",
  correlation: "ಸಹಸಂಬಂಧ",
  correlations: "ಸಹಸಂಬಂಧಗಳು",
  currentCases: "ಪ್ರಸ್ತುತ ಪ್ರಕರಣ(ಗಳು)",
  currentWorkload: "ಪ್ರಸ್ತುತ ಕಾರ್ಯಭಾರ",
  earlyWarning: "ಮುನ್ನೆಚ್ಚರಿಕೆ",
  earlyWarnings: "ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು",
  event: "ಘಟನೆ",
  evidenceHash: "ಸಾಕ್ಷ್ಯ ಹ್ಯಾಶ್",
  fieldCoverageGood: "ವ್ಯಾಪ್ತಿಯಲ್ಲಿರುವ ದಾಖಲೆಗಳಲ್ಲಿ ಅಧಿಕೃತ ವಿಶ್ಲೇಷಣಾ ಕ್ಷೇತ್ರಗಳು ಭರ್ತಿಯಾಗಿವೆ.",
  forecastPending: "ಸೈನ್ ಇನ್ ನಂತರ ಮುನ್ಸೂಚನೆ ಡೇಟಾ ಕಾಣುತ್ತದೆ.",
  high: "ಹೆಚ್ಚು",
  highValueTransfer: "ಹೆಚ್ಚು ಮೌಲ್ಯದ ವರ್ಗಾವಣೆ",
  implemented: "ಅಮಲಾದ",
  investigativeLeads: "ತನಿಖಾ ಸುಳಿವುಗಳು",
  investigationTimeline: "ತನಿಖಾ ಕಾಲರೇಖೆ",
  low: "ಕಡಿಮೆ",
  medium: "ಮಧ್ಯಮ",
  moduleAdmin: "ಸೂಪರ್ ನಿರ್ವಾಹಕ ಬಳಕೆದಾರ ನಿರ್ವಹಣೆ",
  moduleAdvanced: "ಮುನ್ನಡೆದ ಅಪರಾಧ ML, ಹೀಟ್‌ಮ್ಯಾಪ್, ಅಪಾಯ ಮತ್ತು ಅನಾಮಲಿ ಗುಪ್ತಚರ",
  moduleChat: "ಸಂಭಾಷಣಾತ್ಮಕ ಅಪರಾಧ ಗುಪ್ತಚರ ಇಂಟರ್‌ಫೇಸ್",
  moduleDecision: "ನಿರ್ಧಾರ ಬೆಂಬಲ",
  moduleExplain: "ವಿವರಣಾತ್ಮಕ ಎಐ ಮತ್ತು ಸಾಕ್ಷ್ಯ ಹಾದಿಗಳು",
  moduleFinancial: "ಹಣಕಾಸು ವಿಶ್ಲೇಷಣೆ",
  moduleForecast: "ಮುನ್ಸೂಚನೆ ಮತ್ತು ಮುನ್ನೆಚ್ಚರಿಕೆ",
  moduleGeo: "Leaflet ಭೌಗೋಳಿಕ ಅಪರಾಧ ನಕ್ಷೆ ಮತ್ತು ಹೀಟ್ ಲೇಯರ್",
  moduleGovernance: "RBAC, ಡೇಟಾ ಮಾಸ್ಕಿಂಗ್, ದರ ಮಿತಿ, ಸೆಷನ್ ರದ್ದು, ಆಡಿಟ್ ದಾಖಲೆಗಳು",
  moduleLanguage: "ಬಹುಭಾಷಾ, ಧ್ವನಿ ಸಿದ್ಧ, ಪಿಡಿಎಫ್ ಸಂಭಾಷಣೆ ಬೆಂಬಲ",
  moduleNetwork: "ಅಪರಾಧಿ ಜಾಲ ಮತ್ತು ಸಂಬಂಧ ವಿಶ್ಲೇಷಣೆ",
  modulePatterns: "ಅಪರಾಧ ಮಾದರಿ ಪತ್ತೆ",
  moduleProfile: "ಅಪರಾಧಿ ಪ್ರೊಫೈಲಿಂಗ್",
  moduleSearch: "ಹ್ಯಾಶ್-ಪ್ರಿಫಿಕ್ಸ್ ಪ್ರಕರಣ ಹುಡುಕಾಟ",
  moduleSocio: "ಸಮಾಜಶಾಸ್ತ್ರೀಯ ಒಳನೋಟಗಳು",
  moduleTrends: "ಪ್ರವೃತ್ತಿ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಹಾಟ್‌ಸ್ಪಾಟ್‌ಗಳು",
  anomaly: "ಅಸಾಮಾನ್ಯತೆ",
  integratedDataset: "ಸಮಗ್ರ ಡೇಟಾಸೆಟ್",
  mlIncidents: "ಆಮದು ಮಾಡಿದ ಘಟನೆಗಳು",
  riskAreas: "ಅಪಾಯ ಪ್ರದೇಶಗಳು",
  month: "ತಿಂಗಳು",
  nextSteps: "ಮುಂದಿನ ಕ್ರಮಗಳು",
  noCasesForRole: "ಈ ಪಾತ್ರಕ್ಕೆ ಪ್ರಕರಣಗಳು ಲಭ್ಯವಿಲ್ಲ.",
  noClusters: "ಪುನರಾವರ್ತಿತ ಕ್ಲಸ್ಟರ್ ಇಲ್ಲ",
  noClustersBody: "ಅಧಿಕೃತ ದಾಖಲೆಗಳಲ್ಲಿ ಪುನರಾವರ್ತಿತ ಜಿಲ್ಲೆ, ಪ್ರಕಾರ ಅಥವಾ ಕಾರ್ಯ ವಿಧಾನ ಕ್ಲಸ್ಟರ್ ಕಾಣುತ್ತಿಲ್ಲ.",
  noFinancialFindings: "ಪ್ರವೇಶಯೋಗ್ಯ ವಹಿವಾಟುಗಳಿಗೆ ಟ್ರಿಯಾಜ್ ಸೂಚನೆಗಳಿಲ್ಲ.",
  noFindings: "ಸೂಚನೆಗಳಿಲ್ಲ",
  noPatternBars: "ಅಧಿಕೃತ ಪ್ರಕಾರ, MO, ತಿಂಗಳು ಅಥವಾ ಘಟನೆ ಕ್ಷೇತ್ರಗಳು ಇನ್ನೂ ಭರ್ತಿಯಾಗಿಲ್ಲ.",
  none: "ಯಾವುದೂ ಇಲ್ಲ",
  open: "ತೆರೆದ",
  openCases: "ತೆರೆದ ಪ್ರಕರಣಗಳು",
  pending: "ಬಾಕಿ",
  possibleCircularFlow: "ಸಂಭಾವ್ಯ ವಲಯಾಕಾರದ ಹರಿವು",
  possibleStructuring: "ಸಂಭಾವ್ಯ ರಚನೆ",
  projectedPlanning: "ಯೋಜನೆಗಾಗಿ ಅಂದಾಜು",
  reasoningPath: "ತರ್ಕದ ಹಾದಿ",
  riskScore: "ಅಪಾಯ ಅಂಕ",
  similarCases: "ಸಮಾನ ಪ್ರಕರಣಗಳು",
  socialIndicator: "ಸಾಮಾಜಿಕ ಸೂಚಕ",
  suspectAge: "ಆರೋಪಿ ವಯಸ್ಸು",
  suspectGender: "ಆರೋಪಿ ಲಿಂಗ",
  totalAmount: "ಒಟ್ಟು ಮೊತ್ತ",
  transactions: "ವಹಿವಾಟುಗಳು",
  triageSignals: "ಟ್ರಿಯಾಜ್ ಸೂಚನೆಗಳು",
  unavailable: "ಲಭ್ಯವಿಲ್ಲ",
  underReview: "ಪರಿಶೀಲನೆಯಲ್ಲಿ",
  victimAge: "ಬಾಧಿತ ವಯಸ್ಸು",
  victimGender: "ಬಾಧಿತ ಲಿಂಗ",
  visibleFinancialRecords: "ಕಾಣುವ ಹಣಕಾಸು ದಾಖಲೆಗಳು",
  voiceFailed: "ಧ್ವನಿ ಸೆರೆ ಹಿಡಿಯಲು ವಿಫಲವಾಗಿದೆ.",
  voiceUnsupported: "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಇನ್‌ಪುಟ್ ಲಭ್ಯವಿಲ್ಲ.",
});

Object.assign(I18N.en, {
  activityLoaded: "Loaded activity for",
  adminRequiredFields: "Username, full name, district, and temporary password are required.",
  actor: "Actor",
  breachedLimit: "breached",
  breachesAppearHere: "Authenticated user and unauthenticated IP rate-limit breaches will appear here.",
  client: "Client",
  created: "Created",
  deleted: "Deleted",
  deleteUserConfirm: "Delete or disable this account",
  monitoring: "Monitoring",
  noActivityEvents: "No activity events",
  noActivityEventsBody: "No audit events are recorded for this user yet.",
  noAuthorizedAccounts: "No authorized accounts are available.",
  noOpenBreaches: "No open breaches",
  noUsers: "No users",
  passwordPrompt: "Enter a new temporary password with at least 12 characters.",
  passwordResetComplete: "Password reset complete.",
  passwordTooShort: "Temporary password must be at least 12 characters.",
  request: "Request",
  resource: "Resource",
  selectedUser: "Selected user",
  selectUserActivity: "Select the activity button on a user row to monitor account actions.",
  unauthenticatedIp: "Unauthenticated IP",
  userActivity: "User activity",
  withRequests: "with request(s)",
});

Object.assign(I18N.kn, {
  adminRequiredFields: "ಬಳಕೆದಾರ ಹೆಸರು, ಪೂರ್ಣ ಹೆಸರು, ಜಿಲ್ಲೆ ಮತ್ತು ತಾತ್ಕಾಲಿಕ ಪಾಸ್‌ವರ್ಡ್ ಅಗತ್ಯವಿದೆ.",
  breachedLimit: "ಉಲ್ಲಂಘಿಸಿದೆ",
  breachesAppearHere: "ಅಧಿಕೃತ ಬಳಕೆದಾರ ಮತ್ತು ಅನಧಿಕೃತ IP ದರ-ಮಿತಿ ಉಲ್ಲಂಘನೆಗಳು ಇಲ್ಲಿ ಕಾಣುತ್ತವೆ.",
  client: "ಕ್ಲೈಂಟ್",
  created: "ರಚಿಸಲಾಗಿದೆ",
  noAuthorizedAccounts: "ಅಧಿಕೃತ ಖಾತೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
  noOpenBreaches: "ತೆರೆದ ಉಲ್ಲಂಘನೆಗಳಿಲ್ಲ",
  noUsers: "ಬಳಕೆದಾರರಿಲ್ಲ",
  passwordPrompt: "ಕನಿಷ್ಠ 12 ಅಕ್ಷರಗಳ ಹೊಸ ತಾತ್ಕಾಲಿಕ ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ.",
  passwordResetComplete: "ಪಾಸ್‌ವರ್ಡ್ ಮರುಹೊಂದಿಕೆ ಪೂರ್ಣಗೊಂಡಿದೆ.",
  passwordTooShort: "ತಾತ್ಕಾಲಿಕ ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 12 ಅಕ್ಷರಗಳಿರಬೇಕು.",
  request: "ವಿನಂತಿ",
  unauthenticatedIp: "ಅನಧಿಕೃತ IP",
  withRequests: "ವಿನಂತಿ(ಗಳೊಂದಿಗೆ)",
});

Object.assign(I18N.en, {
  authorizedGeocoded: "authorized case(s) include latitude/longitude.",
  googleKeyRequired: "Add a Google Maps JavaScript API key before switching to Google mode.",
  heatLayerActive: "Heat layer is active.",
  heatLayerHidden: "Heat layer hidden",
  heatLayerHiddenBody: "Use the flame control to show authorized geospatial density.",
  mapNotice: "Map notice",
  noHeatData: "No heat map data",
  noOfficialCoordinates: "No official latitude/longitude values found in authorized records.",
  noOfficialCoordinatesTitle: "No official coordinates",
  noOfficialRecordsLoaded: "No official case records are loaded in this database.",
  recordsNoCoordinates: "case record(s) are loaded, but none include latitude and longitude.",
  roleCannotAccess: "This role cannot access the module.",
  disabled: "Disabled",
});

Object.assign(I18N.kn, {
  authorizedGeocoded: "ಅಧಿಕೃತ ಪ್ರಕರಣ(ಗಳು) ಅಕ್ಷಾಂಶ/ರೇಖಾಂಶ ಹೊಂದಿವೆ.",
  googleKeyRequired: "Google ಮೋಡ್‌ಗೆ ಬದಲಿಸುವ ಮೊದಲು Google Maps JavaScript API ಕೀ ಸೇರಿಸಿ.",
  heatLayerActive: "ಹೀಟ್ ಲೇಯರ್ ಸಕ್ರಿಯವಾಗಿದೆ.",
  heatLayerHidden: "ಹೀಟ್ ಲೇಯರ್ ಮರೆಮಾಡಲಾಗಿದೆ",
  heatLayerHiddenBody: "ಅಧಿಕೃತ ಭೌಗೋಳಿಕ ಸಾಂದ್ರತೆಯನ್ನು ತೋರಿಸಲು ಜ್ವಾಲೆ ನಿಯಂತ್ರಣ ಬಳಸಿ.",
  mapNotice: "ನಕ್ಷೆ ಸೂಚನೆ",
  noHeatData: "ಹೀಟ್ ಮ್ಯಾಪ್ ಡೇಟಾ ಇಲ್ಲ",
  noOfficialCoordinates: "ಅಧಿಕೃತ ದಾಖಲೆಗಳಲ್ಲಿ ಅಕ್ಷಾಂಶ/ರೇಖಾಂಶ ಮೌಲ್ಯಗಳಿಲ್ಲ.",
  noOfficialCoordinatesTitle: "ಅಧಿಕೃತ ಸ್ಥಳಾಂಕಗಳಿಲ್ಲ",
  noOfficialRecordsLoaded: "ಈ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಅಧಿಕೃತ ಪ್ರಕರಣ ದಾಖಲೆಗಳು ಲೋಡ್ ಆಗಿಲ್ಲ.",
  recordsNoCoordinates: "ಪ್ರಕರಣ ದಾಖಲೆಗಳು ಲೋಡ್ ಆಗಿವೆ, ಆದರೆ ಯಾವುದರಲ್ಲೂ ಅಕ್ಷಾಂಶ ಮತ್ತು ರೇಖಾಂಶ ಇಲ್ಲ.",
  roleCannotAccess: "ಈ ಪಾತ್ರಕ್ಕೆ ಈ ಮಾಡ್ಯೂಲ್ ಪ್ರವೇಶ ಇಲ್ಲ.",
  disabled: "ನಿಷ್ಕ್ರಿಯ",
});

Object.assign(I18N.kn, {
  autoImportRows: "ಸಾಲುಗಳನ್ನು ಸ್ವಯಂ ಆಮದುಮಾಡಿ",
  biometric: "ಬಯೋಮೆಟ್ರಿಕ್",
  caseFileUpload: "ಪ್ರಕರಣ ಫೈಲ್ ಅಪ್ಲೋಡ್",
  caseSheet: "ಪ್ರಕರಣ ಶೀಟ್",
  chooseFileFirst: "ಮೊದಲು ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ.",
  crimeIntelligencePlatform: "ಬುದ್ಧಿವಂತ ಸಂಭಾಷಣಾತ್ಮಕ ಎಐ ಮತ್ತು ಅಪರಾಧ ವಿಶ್ಲೇಷಣಾ ವೇದಿಕೆ",
  expectedSolution: "ನಿರೀಕ್ಷಿತ ಪರಿಹಾರ ರೂಪರೇಖೆ",
  framework: "ರೂಪರೇಖೆ",
  criminalNetworkDashboard: "ಅಪರಾಧ ಜಾಲ ವಿಶ್ಲೇಷಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
  edgeCsv: "ಎಡ್ಜ್ CSV",
  fingerprintCancelled: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಕ್ರಿಯೆಯನ್ನು ರದ್ದುಪಡಿಸಲಾಗಿದೆ.",
  fingerprintHelp: "Windows Hello, passkey ಅಥವಾ WebAuthn ಹೊಂದಾಣಿಕೆಯ ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಸ್ಕ್ಯಾನರ್ ಬಳಸಿ. ಕಚ್ಚಾ ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಚಿತ್ರಗಳು ಸಾಧನದಿಂದ ಹೊರಬರುವುದಿಲ್ಲ.",
  fingerprintLogin: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಲಾಗಿನ್",
  fingerprintModule: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಮಾಡ್ಯೂಲ್",
  fingerprintPrompt: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಸಾಧನವನ್ನು ಸ್ಪರ್ಶಿಸಿ ಅಥವಾ Windows Hello ಅನುಮೋದಿಸಿ.",
  fingerprintRegistered: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಸಾಧನ ನೋಂದಾಯಿಸಲಾಗಿದೆ.",
  fingerprintSecurity: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಭದ್ರತೆ",
  fingerprintUnsupported: "ಈ ಬ್ರೌಸರ್/ಸಾಧನದಲ್ಲಿ ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಲಾಗಿನ್ ಲಭ್ಯವಿಲ್ಲ.",
  fingerprintUsernameRequired: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಲಾಗಿನ್ ಮೊದಲು ಬಳಕೆದಾರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
  firCopy: "ಎಫ್ಐಆರ್ ಪ್ರತಿಗೆ",
  noFingerprintStorage: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಸಂಗ್ರಹಣೆ ಇಲ್ಲ",
  noFingerprintStorageBody: "ವ್ಯವಸ್ಥೆ ಸಾರ್ವಜನಿಕ credential key ಮತ್ತು sign counter ಮಾತ್ರ ಸಂಗ್ರಹಿಸುತ್ತದೆ; ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಟೆಂಪ್ಲೇಟ್‌ಗಳು ಸಾಧನ/OS ರಕ್ಷಣೆಯಲ್ಲೇ ಇರುತ್ತವೆ.",
  noLinkedCase: "ಲಿಂಕ್ ಮಾಡಿದ ಪ್ರಕರಣ ಇಲ್ಲ",
  nodeCsv: "ನೋಡ್ CSV",
  openFullDashboard: "ಪೂರ್ಣ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ತೆರೆಯಿರಿ",
  pngExport: "PNG ರಫ್ತು",
  professionalSna: "ವೃತ್ತಿಪರ SNA ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
  launchQuery: "ಪ್ರಶ್ನೆ ಪ್ರಾರಂಭಿಸಿ",
  solutionCoverage: "ಪರಿಹಾರ ವ್ಯಾಪ್ತಿ",
  registerFingerprint: "ಫಿಂಗರ್‌ಪ್ರಿಂಟ್ ಸಾಧನ ನೋಂದಾಯಿಸಿ",
  snaDashboard: "SNA ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
  uploadFile: "ಫೈಲ್ ಅಪ್ಲೋಡ್",
  uploadFirOrSheet: "ಎಫ್ಐಆರ್ ಪ್ರತಿಗೆ ಅಥವಾ ಪ್ರಕರಣ ಶೀಟ್ ಅಪ್ಲೋಡ್ ಮಾಡಿ",
  uploading: "ಅಪ್ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
  webauthnOnly: "WebAuthn ಸುರಕ್ಷಿತ ಮೋಡ್",
  webauthnOnlyBody: "ಬ್ರೌಸರ್ ಬೆಂಬಲಿತ ಬಯೋಮೆಟ್ರಿಕ್ authenticator ಗಳೊಂದಿಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ. Vendor-only USB scanner ಗೆ ಸ್ಥಳೀಯ SDK gateway ಅಗತ್ಯ.",
});

Object.assign(I18N.kn, {
  analyzingCrimeData: "ಅಪರಾಧ ದಾಖಲೆಗಳನ್ನು ಓದಿ ಉತ್ತರ ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ...",
  answerSupport: "ಉತ್ತರ ಬೆಂಬಲ",
  crimeDataOnly: "ಅಪರಾಧ ಡೇಟಾ ಮಾತ್ರ",
  crimeRecordsOnly: "ಅಪರಾಧ ದಾಖಲೆಗಳನ್ನು ಮಾತ್ರ ಬಳಸುತ್ತದೆ",
  dataScope: "ಡೇಟಾ ವ್ಯಾಪ್ತಿ",
  evidenceAvailable: "ಸಾಕ್ಷ್ಯ ಲಭ್ಯ",
  evidenceCommand: "KSP AI ಅಪರಾಧ ಸಹಾಯಕ",
  evidenceMode: "ಸಾಕ್ಷ್ಯ ವಿಧಾನ",
  evidenceSources: "ಸಾಕ್ಷ್ಯ ಮೂಲಗಳು",
  filters: "ಫಿಲ್ಟರ್‌ಗಳು",
  importedAggregate: "ಆಮದು ಮಾಡಿದ ಘಟನೆಗಳ ಒಟ್ಟು ವಿಶ್ಲೇಷಣೆ",
  localSearchIndex: "ಸ್ಥಳೀಯ ಪ್ರಕರಣ ಹುಡುಕಾಟ ಸೂಚಿ",
  normalized: "ಸ್ವಚ್ಛಗೊಳಿಸಿದ ಪ್ರಶ್ನೆ",
  noExternalFacts: "ಸಾಕ್ಷ್ಯ ಹಾದಿ ಲಭ್ಯ",
  noIndividualSources: "ಒಟ್ಟು ವಿಶ್ಲೇಷಣೆಯ ಉತ್ತರ. ಈ ಪ್ರಶ್ನೆಗೆ ವೈಯಕ್ತಿಕ ಮೂಲ ಸಾಲುಗಳನ್ನು ತೋರಿಸಲಾಗುವುದಿಲ್ಲ.",
  nlpCleanup: "ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತದೆ",
  oneRecordFound: "1 ದಾಖಲೆ ಕಂಡುಬಂದಿದೆ",
  oneSourceRecord: "1 ಮೂಲ ದಾಖಲೆ",
  orchestrationFlow: "ಆರ್ಕೆಸ್ಟ್ರೇಶನ್ ಹಾದಿ",
  queryInterpretation: "ಪ್ರಶ್ನೆಯ ಅರ್ಥೈಸಿಕೆ",
  queryPlaceholder: "ಸಾಮಾನ್ಯವಾಗಿ ಕೇಳಿ: ಕರ್ನಾಟಕ ಪ್ರಕರಣಗಳನ್ನು ತೋರಿಸಿ, ರವಿ ಕುಮಾರ್ ಹುಡುಕಿ, ಬೆಂಗಳೂರು ಕಳವು ಹಾಟ್‌ಸ್ಪಾಟ್, A1 ಹಣದ ಹಾದಿ...",
  recordsMatched: "ಹೊಂದಿದ ದಾಖಲೆಗಳು",
  recordsFound: "ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿವೆ",
  safeguards: "ರಕ್ಷಣಾ ನಿಯಮಗಳು",
  sourceRecordsLower: "ಮೂಲ ದಾಖಲೆಗಳು",
  sourceRecords: "ಮೂಲ ದಾಖಲೆಗಳು",
  strictCrimeOnly: "ಅಪರಾಧ ದಾಖಲೆಗಳಿಂದ ಉತ್ತರಗಳು",
  selectedModule: "ಆಯ್ದ ಮಾಡ್ಯೂಲ್",
  terms: "ಪದಗಳು",
  unknown: "ಅಜ್ಞಾತ",
  viewEvidenceTrail: "ಸಾಕ್ಷ್ಯ ಮತ್ತು ಪ್ರಶ್ನೆ ಓದಿಕೆ",
});

const state = {
  token: localStorage.getItem("kspToken"),
  user: null,
  panel: "command",
  language: storedLanguage === "kn" ? "kn" : "en",
  theme: storedTheme === "dark" ? "dark" : "light",
  queryLanguage: storedLanguage === "kn" ? "kn" : "en",
  modules: [],
  cases: [],
  trends: null,
  patterns: null,
  advancedCrime: null,
  framework: null,
  network: null,
  selectedNetworkNodeId: null,
  networkCy: null,
  networkPrepared: null,
  networkAnalysisCache: null,
  networkView: {
    mode: "investigation",
    community: "all",
    timePercent: 100,
    pathStart: null,
    pathEnd: null,
    search: "",
    focus: "",
    focusType: "auto",
    renderLimit: 10000,
  },
  socio: null,
  financial: null,
  forecast: null,
  users: [],
  rateLimitAlerts: [],
  rateAlertPoller: null,
  headerClockTimer: null,
  conversationId: null,
  translationMode: "en-kn",
  mapProvider: storedMapProvider === "google" ? "google" : "leaflet",
  googleMapsKey: localStorage.getItem("kspGoogleMapsKey") || "",
  heatEnabled: true,
  leafletMap: null,
  leafletMarkers: [],
  googleMap: null,
  googleMarkers: [],
  fileUploads: [],
  filePreviewUrl: null,
  filePreviewPageUrls: [],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));
sanitizeSensitiveUrl();

function t(key, fallback = key) {
  return I18N[state.language]?.[key] || I18N.en[key] || fallback;
}

function panelTitle(panel) {
  const key = PANEL_KEYS[panel] || panel;
  return t(key, key);
}

function sanitizeSensitiveUrl() {
  const sensitive = new Set(["username", "password", "token", "access_token", "jwt", "secret"]);
  const url = new URL(window.location.href);
  let changed = false;
  for (const key of [...url.searchParams.keys()]) {
    if (sensitive.has(key.toLowerCase())) {
      url.searchParams.delete(key);
      changed = true;
    }
  }
  if (changed) {
    const clean = `${url.pathname}${url.search}${url.hash}`;
    window.history.replaceState({}, document.title, clean || "/");
  }
}

function iconRefresh() {
  if (window.lucide) {
    window.lucide.createIcons();
    return;
  }
  renderFallbackIcons();
}

function renderFallbackIcons() {
  $$("i[data-lucide]").forEach((node) => {
    const name = node.dataset.lucide || "circle";
    const span = document.createElement("span");
    span.className = "fallback-icon";
    span.innerHTML = fallbackIconSvg(name);
    node.replaceWith(span);
  });
}

function fallbackIconSvg(name) {
  const common = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';
  const icon = {
    "activity": '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    "bar-chart-3": '<path d="M4 20V10"/><path d="M12 20V4"/><path d="M20 20v-7"/>',
    "boxes": '<path d="M7 8l5-3 5 3-5 3-5-3Z"/><path d="M7 16l5-3 5 3-5 3-5-3Z"/>',
    "chart-no-axes-combined": '<path d="M4 19l5-6 4 3 7-10"/><path d="M4 5v14h16"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "clipboard-check": '<path d="M9 5h6"/><path d="M9 12l2 2 4-5"/><rect x="5" y="3" width="14" height="18" rx="2"/>',
    "clock-3": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5h4"/>',
    "crosshair": '<circle cx="12" cy="12" r="8"/><path d="M22 12h-4"/><path d="M6 12H2"/><path d="M12 6V2"/><path d="M12 22v-4"/>',
    "external-link": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"/>',
    "file-down": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M12 12v6"/><path d="m9 15 3 3 3-3"/>',
    "file-search": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><circle cx="11" cy="14" r="3"/><path d="m13.5 16.5 2 2"/>',
    "fingerprint": '<path d="M7 17c0-5 10-5 10 0"/><path d="M9 21c0-4 6-4 6 0"/><path d="M5 13c1-8 13-8 14 0"/><path d="M12 3c4 0 8 3 8 8"/>',
    "folder-kanban": '<path d="M3 7h7l2 2h9v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M8 13v3"/><path d="M12 12v5"/><path d="M16 14v2"/>',
    "git-fork": '<circle cx="6" cy="5" r="3"/><circle cx="18" cy="5" r="3"/><circle cx="12" cy="19" r="3"/><path d="M6 8v2a6 6 0 0 0 6 6"/><path d="M18 8v2a6 6 0 0 1-6 6"/>',
    "flame": '<path d="M8.5 14.5A4.5 4.5 0 0 0 17 12c0-4-5-7-5-10-2 2-3 4-3 6 0 1.5.5 2.5.5 2.5S8 9.5 6 7c-.5 2-.5 4 .5 5.5"/>',
    "indian-rupee": '<path d="M6 3h12"/><path d="M6 8h12"/><path d="M13 21 6 13h4a5 5 0 0 0 0-10"/>',
    "image-down": '<rect x="3" y="3" width="18" height="14" rx="2"/><path d="m3 14 4-4 5 5 3-3 6 6"/><path d="M12 17v6"/><path d="m9 20 3 3 3-3"/>',
    "key-round": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m12 11 8-8"/><path d="m17 3 4 4"/><path d="m15 5 4 4"/>',
    "landmark": '<path d="M3 21h18"/><path d="M5 10h14"/><path d="M6 10v8"/><path d="M10 10v8"/><path d="M14 10v8"/><path d="M18 10v8"/><path d="M12 3 4 8h16Z"/>',
    "languages": '<path d="M5 8h8"/><path d="M9 4v4c0 5-2 8-5 10"/><path d="M7 14c2 1 4 2 7 2"/><path d="M17 10l4 10"/><path d="M15 16h5"/>',
    "layers": '<path d="m12 2 9 5-9 5-9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    "layout-dashboard": '<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
    "list-checks": '<path d="m3 7 2 2 4-4"/><path d="M11 7h10"/><path d="m3 17 2 2 4-4"/><path d="M11 17h10"/>',
    "log-in": '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/>',
    "map": '<path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z"/><path d="M9 3v15"/><path d="M15 6v15"/>',
    "map-pinned": '<path d="M9 18 3 21V6l6-3 6 3 6-3v15l-6 3-6-3Z"/><path d="M15 6v15"/><path d="M9 3v15"/><circle cx="17" cy="9" r="2"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "message-square-text": '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/><path d="M8 8h8"/><path d="M8 12h6"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 7.5A9 9 0 1 1 12 3Z"/>',
    "network": '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><path d="M8.5 7.5 11 15"/><path d="m15.5 7.5-3 7.5"/><path d="M9 6h6"/>',
    "panel-left-close": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/><path d="m16 10-3 2 3 2"/>',
    "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
    "radar": '<path d="M13 2a10 10 0 1 1-8 16"/><path d="M12 12 20 4"/><circle cx="12" cy="12" r="3"/>',
    "refresh-cw": '<path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "repeat-2": '<path d="m17 2 4 4-4 4"/><path d="M3 11V9a3 3 0 0 1 3-3h15"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a3 3 0 0 1-3 3H3"/>',
    "scan-search": '<path d="M7 3H5a2 2 0 0 0-2 2v2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="11" cy="11" r="3"/><path d="m13.5 13.5 3 3"/>',
    "scroll-text": '<path d="M8 21h8a4 4 0 0 0 4-4V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v12a4 4 0 0 0 4 4Z"/><path d="M8 7h8"/><path d="M8 11h8"/><path d="M8 15h5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "share-2": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4"/><path d="m15.4 6.5-6.8 4"/>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-5"/>',
    "sparkles": '<path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7Z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "table": '<path d="M3 5h18v16H3Z"/><path d="M3 11h18"/><path d="M9 5v16"/>',
    "table-properties": '<path d="M3 5h18v16H3Z"/><path d="M3 11h18"/><path d="M9 5v16"/><path d="M13 15h5"/><path d="M13 18h5"/>',
    "user-round": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "user-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6"/><path d="M22 11h-6"/>',
    "user-search": '<circle cx="10" cy="8" r="4"/><path d="M2 21a8 8 0 0 1 13-6"/><circle cx="18" cy="18" r="3"/><path d="m21 21-1-1"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "wallet-cards": '<path d="M3 7h15a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H5a2 2 0 0 1-2-2Z"/><path d="M3 7V5a2 2 0 0 1 2-2h12"/><path d="M16 14h2"/>',
  }[name] || '<circle cx="12" cy="12" r="8"/>';
  return `<svg ${common}>${icon}</svg>`;
}

function setText(selector, value) {
  const node = $(selector);
  if (node) node.textContent = value;
}

function applyTranslations() {
  document.documentElement.lang = state.language === "kn" ? "kn" : "en";
  $$("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n, node.textContent);
  });
  $$("[data-i18n-placeholder]").forEach((node) => {
    node.setAttribute("placeholder", t(node.dataset.i18nPlaceholder, node.getAttribute("placeholder") || ""));
  });
  $$("[data-i18n-title]").forEach((node) => {
    const value = t(node.dataset.i18nTitle, node.getAttribute("title") || "");
    node.setAttribute("title", value);
    node.setAttribute("aria-label", value);
  });
  $$("[data-ui-lang]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.uiLang === state.language);
  });
  if ($("#queryLanguage")) {
    $("#queryLanguage").value = state.queryLanguage;
  }
  setText("#panelTitle", panelTitle(state.panel));
}

function setLanguage(language) {
  state.language = language === "kn" ? "kn" : "en";
  state.queryLanguage = state.language;
  localStorage.setItem("kspUiLanguage", state.language);
  applyTranslations();
  applyTheme(state.theme);
  checkHealth();
  renderOverview();
  renderFramework();
  renderModules();
  renderCases();
  renderFileUploads();
  renderTrends();
  renderPatterns();
  renderSociological();
  renderFinancial();
  renderForecast();
  renderHotspots();
  renderMapInsights();
  renderRateLimitAlerts();
  iconRefresh();
}

function applyTheme(theme) {
  state.theme = theme === "dark" ? "dark" : "light";
  document.documentElement.dataset.theme = state.theme;
  document.documentElement.style.colorScheme = state.theme;
  localStorage.setItem("kspTheme", state.theme);
  const dark = state.theme === "dark";
  $$("[data-theme-toggle]").forEach((button) => {
    button.classList.toggle("is-active", dark);
    button.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    button.setAttribute("title", dark ? "Switch to light mode" : "Switch to dark mode");
    const iconName = dark ? "sun" : "moon";
    let icon = button.querySelector("[data-theme-icon]");
    if (!icon || icon.tagName.toLowerCase() !== "i") {
      icon?.remove();
      icon = document.createElement("i");
      icon.dataset.themeIcon = "";
      button.insertBefore(icon, button.firstChild);
    }
    icon.dataset.lucide = iconName;
    const label = button.querySelector("[data-theme-label]");
    if (label) {
      const compact = button.classList.contains("compact");
      label.textContent = dark ? (compact ? "Light" : "Light mode") : (compact ? "Dark" : "Dark mode");
    }
  });
  iconRefresh();
}

function toggleTheme() {
  applyTheme(state.theme === "dark" ? "light" : "dark");
}

async function api(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const headers = {
    ...(options.headers || {}),
  };
  if (!isFormData) headers["Content-Type"] = "application/json";
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(path, { ...options, headers });
  if (response.status === 401) {
    clearSession();
  }
  if (!response.ok) {
    let message = response.statusText;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch (_error) {
      message = response.statusText;
    }
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

function showView(name) {
  $("[data-view='login']").classList.toggle("is-hidden", name !== "login");
  $("[data-view='shell']").classList.toggle("is-hidden", name !== "shell");
  document.body.classList.toggle("login-view-active", name === "login");
}

function clearSession() {
  state.token = null;
  state.user = null;
  localStorage.removeItem("kspToken");
  stopRateAlertPolling();
  showView("login");
}

async function boot() {
  initCursorGlow();
  startHeaderClock();
  applyTheme(state.theme);
  bindEvents();
  applyTranslations();
  await checkHealth();
  if (state.token) {
    try {
      state.user = await api("/auth/me");
      showView("shell");
      await loadAll();
    } catch (_error) {
      clearSession();
    }
  } else {
    showView("login");
  }
  applyTranslations();
  iconRefresh();
}

function initCursorGlow() {
  if (window.matchMedia("(pointer: coarse)").matches || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  const glow = document.createElement("div");
  glow.className = "cursor-glow";
  document.body.appendChild(glow);
  let frame = null;
  let nextX = -999;
  let nextY = -999;
  const update = () => {
    glow.style.setProperty("--cursor-x", `${nextX}px`);
    glow.style.setProperty("--cursor-y", `${nextY}px`);
    frame = null;
  };
  window.addEventListener("pointermove", (event) => {
    if (!document.body.classList.contains("login-view-active") || !event.target.closest?.(".login-screen")) {
      glow.classList.remove("is-visible");
      return;
    }
    nextX = event.clientX;
    nextY = event.clientY;
    glow.classList.add("is-visible");
    if (frame === null) frame = window.requestAnimationFrame(update);
  });
  window.addEventListener("pointerleave", () => {
    glow.classList.remove("is-visible");
  });
}

function startHeaderClock() {
  updateHeaderClock();
  if (state.headerClockTimer) return;
  state.headerClockTimer = window.setInterval(updateHeaderClock, 1000);
}

function updateHeaderClock() {
  const now = new Date();
  setText("#headerClock", now.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit" }));
}

function updateCommandHeader() {
  const cases = state.cases || [];
  const openCases = cases.filter((item) => String(item.status || "").toLowerCase() === "open").length;
  const importedIncidents = Number(state.advancedCrime?.imported_count || 0);
  const liveCases = importedIncidents || cases.length;
  const riskAreas = state.advancedCrime?.risk_areas?.length || state.forecast?.hotspots?.length || 0;
  const clusters =
    state.patterns?.clusters?.length ||
    state.advancedCrime?.emerging_trend_alerts?.length ||
    Math.max(0, Math.round((state.network?.links?.length || 0) / 6));
  const financialFindings = state.financial?.findings?.length || 0;
  const forecastAlerts = (state.forecast?.hotspots?.length || 0) + (state.forecast?.early_warnings?.length || 0);
  const fraudCases = countCasesMatching(["fraud", "cheating", "money", "financial", "transaction"]);
  const cyberCases = countCasesMatching(["cyber", "online", "digital", "upi", "account"]);
  const highRiskSubjects = riskAreas || countHighRiskNetworkSubjects();
  const role = state.user ? labelValue(state.user.role) : "Secure session";
  const district = state.user?.district || "State HQ";

  setText("#commandScope", `${district} | ${role}`);
  setText("#contextRoleDistrict", `${district} | ${role}`);
  setText("#headerLiveCases", formatCount(liveCases));
  setText("#headerOpenFirs", formatCount(openCases));
  setText("#headerHighRiskSubjects", formatCount(highRiskSubjects));
  setText("#headerNetworkClusters", formatCount(clusters));
  setText("#contextActiveInvestigations", formatCount(openCases || cases.length));
  setText("#contextOpenFirs", formatCount(openCases));
  setText("#contextFraudCases", formatCount(fraudCases || financialFindings));
  setText("#contextCyberCases", formatCount(cyberCases));
  setText("#contextForecastAlerts", formatCount(forecastAlerts));
  setText("#contextEmergingClusters", formatCount(clusters));
  setText("#contextHighRiskSubjects", formatCount(highRiskSubjects));
  setText("#navBadgeCases", formatCount(cases.length));
  setText("#navBadgeAnalytics", formatCount(riskAreas || forecastAlerts));
  setText("#navBadgeNetwork", formatCount(state.network?.nodes?.length || 0));
  setText("#navBadgeFinancial", formatCount(financialFindings));
  setText("#navBadgePatterns", formatCount(clusters));
  setText("#headerAuditStatus", state.token ? "Audit armed" : "Audit locked");
}

function countCasesMatching(terms) {
  const loweredTerms = terms.map((term) => term.toLowerCase());
  return (state.cases || []).filter((item) => {
    const haystack = [
      item.case_type,
      item.crime_type,
      item.summary,
      item.modus_operandi,
      item.suspect_name,
      item.victim_name,
      item.complainant_name,
    ].filter(Boolean).join(" ").toLowerCase();
    return loweredTerms.some((term) => haystack.includes(term));
  }).length;
}

function countHighRiskNetworkSubjects() {
  return (state.network?.nodes || []).filter((node) => {
    const risk = Number(node.risk_score || node.metadata?.risk_score || 0);
    return node.type === "suspect" && risk >= 70;
  }).length;
}

function bindEvents() {
  $("#loginForm").addEventListener("submit", handleLogin);
  $("#fingerprintLoginBtn")?.addEventListener("click", handleFingerprintLogin);
  $("#logoutBtn").addEventListener("click", handleLogout);
  $("#sidebarToggle").addEventListener("click", toggleSidebar);
  $("#mobileMenu").addEventListener("click", toggleMobileSidebar);
  $("#refreshCases").addEventListener("click", loadCases);
  $("#caseSearchInput").addEventListener("input", debounce(handleCaseSearch, 120));
  $("#caseFileUploadForm")?.addEventListener("submit", uploadCaseFile);
  $("#uploadType")?.addEventListener("change", renderUploadControls);
  $("#refreshFileUploads")?.addEventListener("click", () => loadFileUploads());
  $("#fileLookupInput")?.addEventListener("input", debounce(handleFileLookup, 160));
  $("#closeFilePreview")?.addEventListener("click", closeFilePreview);
  $("#registerFingerprintBtn")?.addEventListener("click", registerFingerprint);
  $("#queryForm").addEventListener("submit", handleQuery);
  $("#globalSearchForm")?.addEventListener("submit", handleGlobalSearch);
  $("#globalFab")?.addEventListener("click", () => {
    setPanel("command");
    $("#queryInput")?.focus();
  });
  $("#newConversation").addEventListener("click", createConversation);
  $("#translateBtn").addEventListener("click", handleTranslate);
  $("#closeTranslationModal")?.addEventListener("click", closeTranslationModal);
  $("#exportPdfBtn").addEventListener("click", exportPdf);
  $("#profileBtn").addEventListener("click", loadProfile);
  $("#supportBtn").addEventListener("click", loadSupport);
  $("#explainBtn").addEventListener("click", loadExplanation);
  $("#auditRefresh").addEventListener("click", loadAudit);
  $("#localMapBtn").addEventListener("click", () => switchMapProvider("leaflet"));
  $("#googleMapBtn").addEventListener("click", () => switchMapProvider("google"));
  $("#heatToggleBtn").addEventListener("click", toggleHeatLayer);
  $("#saveMapKey").addEventListener("click", saveGoogleMapsKey);
  $("#networkFocusApply")?.addEventListener("click", applyNetworkFocus);
  $("#networkFocusClear")?.addEventListener("click", clearNetworkFocus);
  $("#networkFocusInput")?.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      applyNetworkFocus();
    }
  });
  $("#networkFocusType")?.addEventListener("change", (event) => {
    state.networkView.focusType = event.target.value || "auto";
  });
  $("#networkSearchInput")?.addEventListener("input", debounce(handleNetworkSearch, 140));
  $("#networkCommunitySelect")?.addEventListener("change", (event) => {
    state.networkView.community = event.target.value || "all";
    renderNetwork();
  });
  $("#networkTimeSlider")?.addEventListener("input", (event) => {
    state.networkView.timePercent = Number(event.target.value || 100);
    renderNetwork();
  });
  $("#networkPanelClose")?.addEventListener("click", () => closeNetworkPanel());
  $$("[data-network-mode]").forEach((button) => {
    button.addEventListener("click", () => setNetworkMode(button.dataset.networkMode || "investigation"));
  });
  $$("[data-network-export]").forEach((button) => {
    button.addEventListener("click", () => exportNetwork(button.dataset.networkExport));
  });
  $("#refreshUsers").addEventListener("click", loadUsers);
  $("#createUserForm").addEventListener("submit", createAdminUser);
  $("#refreshRateAlerts").addEventListener("click", () => loadRateLimitAlerts(true));
  $("#queryLanguage")?.addEventListener("change", (event) => {
    state.queryLanguage = event.target.value === "kn" ? "kn" : "en";
  });
  $("#voiceBtn")?.addEventListener("click", startVoiceQuery);
  $("#clearChatBtn")?.addEventListener("click", clearConversationView);
  $("#attachFromChatBtn")?.addEventListener("click", () => {
    setPanel("cases");
    $("#caseFileInput")?.focus();
  });
  $("#translateFromChatBtn")?.addEventListener("click", () => {
    openTranslationModal();
  });
  $$("[data-query-template]").forEach((button) => {
    button.addEventListener("click", () => launchAssistantChip(button.dataset.queryTemplate || ""));
  });
  document.addEventListener("click", handleAssistantActionClick);
  window.addEventListener("resize", debounce(() => {
    if (state.panel === "map") drawHeatCanvas();
    if (state.panel === "network") renderNetwork();
  }, 120));

  $$("[data-ui-lang]").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.uiLang));
  });

  $$("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", toggleTheme);
  });

  $$(".nav-item").forEach((button) => {
    button.addEventListener("click", () => setPanel(button.dataset.panel));
  });

  $$(".bottom-nav-item").forEach((button) => {
    button.addEventListener("click", () => setPanel(button.dataset.panel));
  });

  $$("[data-panel-jump]").forEach((button) => {
    button.addEventListener("click", () => setPanel(button.dataset.panelJump));
  });

  $$(".segmented button").forEach((button) => {
    button.addEventListener("click", () => {
      state.translationMode = button.dataset.translate;
      $$(".segmented button").forEach((item) => item.classList.remove("is-active"));
      button.classList.add("is-active");
    });
  });
}

function toggleSidebar() {
  $("#shell").classList.toggle("sidebar-collapsed");
}

function toggleMobileSidebar() {
  $("#shell").classList.toggle("sidebar-open");
}

async function handleLogin(event) {
  event.preventDefault();
  setText("#loginError", "");
  try {
    const body = {
      username: $("#username").value.trim(),
      password: $("#password").value,
    };
    const login = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    });
    await establishSession(login);
  } catch (error) {
    setText("#loginError", error.message);
  }
}

async function establishSession(login) {
  state.token = login.access_token;
  state.user = login.user;
  localStorage.setItem("kspToken", state.token);
  showView("shell");
  await loadAll();
}

function supportsWebAuthn() {
  return Boolean(window.PublicKeyCredential && navigator.credentials);
}

function base64UrlToBuffer(value) {
  const normalized = String(value || "").replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "=".repeat((4 - (normalized.length % 4)) % 4);
  const binary = window.atob(padded);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes.buffer;
}

function bufferToBase64Url(buffer) {
  if (!buffer) return "";
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let index = 0; index < bytes.byteLength; index += 1) {
    binary += String.fromCharCode(bytes[index]);
  }
  return window.btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function clonePublicKeyOptions(options) {
  return JSON.parse(JSON.stringify(options.publicKey || {}));
}

function prepareCredentialCreationOptions(options) {
  const publicKey = clonePublicKeyOptions(options);
  publicKey.challenge = base64UrlToBuffer(publicKey.challenge);
  publicKey.user.id = base64UrlToBuffer(publicKey.user.id);
  publicKey.excludeCredentials = (publicKey.excludeCredentials || []).map((credential) => ({
    ...credential,
    id: base64UrlToBuffer(credential.id),
  }));
  return publicKey;
}

function prepareCredentialRequestOptions(options) {
  const publicKey = clonePublicKeyOptions(options);
  publicKey.challenge = base64UrlToBuffer(publicKey.challenge);
  publicKey.allowCredentials = (publicKey.allowCredentials || []).map((credential) => ({
    ...credential,
    id: base64UrlToBuffer(credential.id),
  }));
  return publicKey;
}

function serializePublicKeyCredential(credential) {
  const response = credential.response;
  const payload = {
    id: credential.id,
    rawId: bufferToBase64Url(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: bufferToBase64Url(response.clientDataJSON),
    },
  };
  if (response.attestationObject) {
    payload.response.attestationObject = bufferToBase64Url(response.attestationObject);
    payload.response.transports = response.getTransports ? response.getTransports() : [];
  }
  if (response.authenticatorData) {
    payload.response.authenticatorData = bufferToBase64Url(response.authenticatorData);
    payload.response.signature = bufferToBase64Url(response.signature);
    payload.response.userHandle = bufferToBase64Url(response.userHandle);
  }
  return payload;
}

async function registerFingerprint() {
  const resultNode = $("#fingerprintRegisterResult");
  if (!supportsWebAuthn()) {
    setText("#fingerprintRegisterResult", t("fingerprintUnsupported"));
    return;
  }
  setText("#fingerprintRegisterResult", t("checking"));
  try {
    const options = await api("/auth/fingerprint/register/options", {
      method: "POST",
      body: JSON.stringify({}),
    });
    setText("#fingerprintRegisterResult", t("fingerprintPrompt", "Touch your fingerprint device or approve Windows Hello."));
    const credential = await navigator.credentials.create({
      publicKey: prepareCredentialCreationOptions(options),
    });
    if (!credential) throw new Error(t("fingerprintCancelled", "Fingerprint registration was cancelled."));
    const verified = await api("/auth/fingerprint/register/verify", {
      method: "POST",
      body: JSON.stringify(serializePublicKeyCredential(credential)),
    });
    if (resultNode) {
      resultNode.innerHTML = `
        <strong>${escapeHtml(t("fingerprintRegistered"))}</strong>
        <p>${escapeHtml(shorten(verified.credential_id, 32))}</p>
      `;
    }
  } catch (error) {
    setText("#fingerprintRegisterResult", error.message);
  }
}

async function handleFingerprintLogin() {
  setText("#loginError", "");
  if (!supportsWebAuthn()) {
    setText("#loginError", t("fingerprintUnsupported"));
    return;
  }
  const username = $("#username").value.trim();
  if (!username) {
    setText("#loginError", t("fingerprintUsernameRequired", "Enter username before fingerprint login."));
    $("#username").focus();
    return;
  }
  try {
    const options = await api("/auth/fingerprint/login/options", {
      method: "POST",
      body: JSON.stringify({ username }),
    });
    setText("#loginError", t("fingerprintPrompt", "Touch your fingerprint device or approve Windows Hello."));
    const credential = await navigator.credentials.get({
      publicKey: prepareCredentialRequestOptions(options),
    });
    if (!credential) throw new Error(t("fingerprintCancelled", "Fingerprint login was cancelled."));
    const login = await api("/auth/fingerprint/login/verify", {
      method: "POST",
      body: JSON.stringify(serializePublicKeyCredential(credential)),
    });
    setText("#loginError", "");
    await establishSession(login);
  } catch (error) {
    setText("#loginError", error.message);
  }
}

async function handleLogout() {
  try {
    if (state.token) await api("/auth/logout", { method: "POST" });
  } catch (_error) {
    // Local cleanup still matters if the token has already expired.
  }
  clearSession();
}

async function checkHealth() {
  try {
    const health = await fetch("/health").then((response) => response.json());
    setText("#apiStatus", health.status === "ok" ? t("apiOnline") : t("apiCheck"));
  } catch (_error) {
    setText("#apiStatus", t("apiOffline"));
  }
}

async function loadAll() {
  updateUserChrome();
  await Promise.allSettled([
    loadModules(),
    loadFramework(),
    loadCases(),
    loadFileUploads(),
    loadTrends(),
    loadPatterns(),
    loadAdvancedCrime(),
    loadNetwork(),
    loadSociological(),
    loadFinancial(),
    loadForecast(),
    loadAudit(),
    isSuperAdmin() ? loadUsers() : Promise.resolve(),
    isSuperAdmin() ? loadRateLimitAlerts(false) : Promise.resolve(),
  ]);
  renderOverview();
  setPanel(state.panel || "command");
  iconRefresh();
}

function updateUserChrome() {
  const label = state.user ? `${state.user.full_name} - ${labelValue(state.user.role)}` : t("checking");
  setText("#userLabel", label);
  setText("#sessionLabel", state.user ? `${state.user.district} / ${labelValue(state.user.role)}` : t("intelligentSystems"));
  updateCommandHeader();
  $$(".admin-only").forEach((node) => node.classList.toggle("is-hidden", !isSuperAdmin()));
  if (isSuperAdmin()) {
    startRateAlertPolling();
  } else {
    stopRateAlertPolling();
  }
  if (!isSuperAdmin() && state.panel === "admin") {
    setPanel("overview");
  }
}

function isSuperAdmin() {
  return state.user?.role === "super_admin";
}

function setPanel(panel) {
  if (panel === "admin" && !isSuperAdmin()) {
    panel = "overview";
  }
  state.panel = panel;
  $("#shell")?.setAttribute("data-active-panel", panel);
  $$(".nav-item").forEach((item) => item.classList.toggle("is-active", item.dataset.panel === panel));
  $$(".bottom-nav-item").forEach((item) => item.classList.toggle("is-active", item.dataset.panel === panel));
  $$(".panel").forEach((item) => item.classList.toggle("is-active", item.id === panel));
  setText("#panelTitle", panelTitle(panel));
  if (panel === "network") renderNetwork();
  if (panel === "framework") renderFramework();
  if (panel === "patterns") renderPatterns();
  if (panel === "map") renderCrimeMap();
  if (panel === "admin") {
    loadUsers();
    loadRateLimitAlerts(false);
  }
  $("#shell").classList.remove("sidebar-open");
  iconRefresh();
}

function openTranslationModal() {
  const modal = $("#translationModal");
  if (!modal) return;
  modal.classList.remove("is-hidden");
  modal.classList.add("is-open");
  $("#translateInput")?.focus();
  iconRefresh();
}

function closeTranslationModal() {
  const modal = $("#translationModal");
  if (!modal) return;
  modal.classList.add("is-hidden");
  modal.classList.remove("is-open");
}

async function loadModules() {
  state.modules = await api("/modules");
  renderModules();
}

async function loadFramework() {
  state.framework = await api("/framework");
  renderFramework();
}

async function loadCases() {
  state.cases = await api("/cases");
  renderCases();
  renderCaseSelect();
  renderOverview();
}

async function handleCaseSearch() {
  const query = $("#caseSearchInput").value.trim();
  if (query.length < 2) {
    setText("#searchLatency", "Indexed hash-prefix search");
    await loadCases();
    return;
  }
  try {
    const response = await api(`/cases/search?q=${encodeURIComponent(query)}&limit=25`);
    state.cases = response.results.map((item) => item.case);
    renderCases();
    renderCaseSelect();
    setText("#searchLatency", `${response.result_count} result(s) / ${response.elapsed_ms.toFixed(2)} ms`);
  } catch (error) {
    setText("#searchLatency", error.message);
  }
}

function renderUploadControls() {
  const uploadType = $("#uploadType")?.value || "case_sheet";
  const autoImport = $("#uploadAutoImport");
  const caseSelect = $("#uploadCaseId");
  if (autoImport) {
    autoImport.disabled = uploadType !== "case_sheet";
    autoImport.checked = uploadType === "case_sheet" ? autoImport.checked : false;
  }
  if (caseSelect) {
    caseSelect.disabled = uploadType !== "fir_copy";
  }
}

async function uploadCaseFile(event) {
  event.preventDefault();
  const fileInput = $("#caseFileInput");
  const file = fileInput?.files?.[0];
  if (!file) {
    setText("#uploadResult", t("chooseFileFirst"));
    return;
  }
  const uploadType = $("#uploadType").value;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("upload_type", uploadType);
  formData.append("source_system", $("#uploadSourceSystem").value.trim() || "uploaded-case-file");
  formData.append("auto_import", $("#uploadAutoImport").checked ? "true" : "false");
  if (uploadType === "fir_copy" && $("#uploadCaseId").value) {
    formData.append("case_id", $("#uploadCaseId").value);
  }
  setText("#uploadResult", t("uploading"));
  try {
    const result = await api("/files/upload", {
      method: "POST",
      body: formData,
    });
    $("#caseFileUploadForm").reset();
    $("#uploadSourceSystem").value = "uploaded-case-file";
    renderUploadControls();
    $("#uploadResult").innerHTML = `
      <strong>${escapeHtml(labelValue(result.status))}</strong>
      <p>${escapeHtml(result.filename)} / ${escapeHtml(String(result.size_bytes))} bytes</p>
      <p>${escapeHtml(t("imported"))}: ${result.imported} / ${escapeHtml(t("skipped"))}: ${result.skipped}</p>
      <p>SHA-256: ${escapeHtml(shorten(result.sha256, 24))}</p>
      ${(result.notes || []).map((note) => `<p>${escapeHtml(note)}</p>`).join("")}
    `;
    await loadCases();
    await loadFileUploads();
    await Promise.allSettled([loadTrends(), loadNetwork(), loadFinancial(), loadForecast()]);
  } catch (error) {
    $("#uploadResult").innerHTML = `<p>${escapeHtml(error.message)}</p>`;
  }
}

async function loadFileUploads(query = $("#fileLookupInput")?.value.trim() || "") {
  const rowsTarget = $("#fileUploadRows");
  try {
    const uploads = await api(`/files/uploads?q=${encodeURIComponent(query)}&limit=80`);
    state.fileUploads = uploads;
    renderFileUploads();
    renderCases();
  } catch (error) {
    state.fileUploads = [];
    if (rowsTarget) rowsTarget.innerHTML = `<p class="muted-copy">${escapeHtml(error.message)}</p>`;
    setText("#fileLookupStatus", error.message);
  }
}

async function handleFileLookup() {
  await loadFileUploads($("#fileLookupInput")?.value.trim() || "");
}

function renderFileUploads() {
  const target = $("#fileUploadRows");
  if (!target) return;
  setText("#fileLookupStatus", `${state.fileUploads.length} file(s)`);
  target.innerHTML = state.fileUploads.length
    ? state.fileUploads.map(fileUploadCard).join("")
    : `<p class="muted-copy">${escapeHtml(t("noUploadedFiles"))}</p>`;
  $$("[data-file-preview]").forEach((button) => {
    button.addEventListener("click", () => previewFileUpload(button.dataset.filePreview));
  });
  $$("[data-file-xml]").forEach((button) => {
    button.addEventListener("click", () => downloadFirXml(button.dataset.fileXml));
  });
  iconRefresh();
}

function fileUploadCard(upload) {
  const linked = [upload.linked_fir_number, upload.linked_district].filter(Boolean).join(" / ");
  const date = upload.uploaded_at ? new Date(upload.uploaded_at).toLocaleString() : "";
  return `
    <article class="file-upload-row">
      <button type="button" class="file-upload-main" data-file-preview="${escapeHtml(upload.id)}">
        <strong>${escapeHtml(upload.original_filename)}</strong>
        <span>${escapeHtml(linked || upload.upload_type)}${date ? ` / ${escapeHtml(date)}` : ""}</span>
      </button>
      <div class="file-upload-meta">
        ${statusBadge(upload.status)}
        <span>${escapeHtml(prettyBytes(upload.size_bytes))}</span>
        <span>${escapeHtml((upload.extension || "").toUpperCase())}</span>
      </div>
      <button type="button" class="secondary-action compact-action" data-file-preview="${escapeHtml(upload.id)}">
        <i data-lucide="eye"></i><span>${escapeHtml(t("previewFile"))}</span>
      </button>
      ${upload.fir_reconstruction_status ? `
        <button type="button" class="secondary-action compact-action" data-file-xml="${escapeHtml(upload.id)}">
          <i data-lucide="file-code-2"></i><span>FIR XML</span>
        </button>
      ` : ""}
    </article>
  `;
}

async function downloadFirXml(uploadId) {
  try {
    const response = await fetch(`/files/uploads/${encodeURIComponent(uploadId)}/fir.xml`, {
      headers: state.token ? { Authorization: `Bearer ${state.token}` } : {},
    });
    if (!response.ok) throw new Error(response.statusText || "FIR XML download failed");
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const upload = state.fileUploads.find((item) => item.id === uploadId);
    const baseName = (upload?.original_filename || uploadId).replace(/\.[^.]+$/, "");
    const link = document.createElement("a");
    link.href = url;
    link.download = `${baseName}-fir-reconstruction.xml`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    setText("#fileLookupStatus", error.message);
  }
}

function openFilePreviewDrawer() {
  $("#caseFilePreviewDrawer")?.classList.remove("is-hidden");
  $("#filePreviewPanel")?.classList.add("is-open");
}

function revokeFilePreviewUrls() {
  const urls = new Set();
  if (state.filePreviewUrl) {
    urls.add(state.filePreviewUrl);
    state.filePreviewUrl = null;
  }
  (state.filePreviewPageUrls || []).forEach((url) => urls.add(url));
  urls.forEach((url) => URL.revokeObjectURL(url));
  state.filePreviewPageUrls = [];
}

async function loadFilePreviewPages(uploadId) {
  try {
    return await api(`/files/uploads/${encodeURIComponent(uploadId)}/pages`);
  } catch (_error) {
    return { page_count: 1, visible_pages: [1] };
  }
}

function renderFilePreviewPages(uploadId, meta, activePage = 1) {
  const target = $("#filePreviewPages");
  if (!target) return;
  const pageCount = Math.max(1, Number(meta?.page_count || 1));
  const pages = (meta?.visible_pages || Array.from({ length: Math.min(5, pageCount) }, (_, index) => index + 1))
    .map((page) => Number(page))
    .filter((page) => Number.isFinite(page) && page >= 1);
  if (pageCount <= 1 || pages.length <= 1) {
    target.hidden = true;
    target.innerHTML = "";
    return;
  }
  target.hidden = false;
  target.innerHTML = `
    <span>Pages</span>
    <div class="file-preview-page-scroll">
      ${pages.map((page) => `
        <button type="button" class="${page === activePage ? "is-active" : ""}" data-preview-page="${page}" data-preview-upload="${escapeHtml(uploadId)}">
          ${page}
        </button>
      `).join("")}
    </div>
    ${pageCount > 5 ? `<small>Showing 1-5 of ${pageCount}</small>` : ""}
  `;
  $$("[data-preview-page]").forEach((button) => {
    button.addEventListener("click", () => previewFileUpload(button.dataset.previewUpload, Number(button.dataset.previewPage || 1)));
  });
}

async function previewFileUpload(uploadId, page = 1) {
  let upload = state.fileUploads.find((item) => item.id === uploadId);
  if (!upload) {
    try {
      upload = await api(`/files/uploads/${encodeURIComponent(uploadId)}`);
      state.fileUploads = [upload, ...(state.fileUploads || []).filter((item) => item.id !== uploadId)];
    } catch (_error) {
      return;
    }
  }
  const frame = $("#filePreviewFrame");
  const fallback = $("#filePreviewFallback");
  if (!frame || !fallback) return;
  const image = $("#filePreviewImage");
  openFilePreviewDrawer();
  closeFilePreview(false);
  setText("#filePreviewTitle", upload.original_filename);
  setText("#filePreviewMeta", fileUploadMeta(upload));
  setText("#fileLookupStatus", `Previewing ${upload.original_filename}`);
  fallback.classList.remove("is-visible");
  fallback.textContent = "";

  const extension = String(upload.extension || "").toLowerCase();
  if ([".pdf", ".doc", ".docx"].includes(extension)) {
    const pageMeta = await loadFilePreviewPages(uploadId);
    const safePage = Math.max(1, Math.min(Number(page || 1), Number(pageMeta?.page_count || page || 1)));
    renderFilePreviewPages(uploadId, pageMeta, safePage);
    try {
      const response = await fetch(`/files/uploads/${encodeURIComponent(uploadId)}/render.png?page=${encodeURIComponent(safePage)}`, {
        headers: state.token ? { Authorization: `Bearer ${state.token}` } : {},
      });
      if (!response.ok) throw new Error(response.statusText || t("filePreviewFailed"));
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      state.filePreviewUrl = url;
      state.filePreviewPageUrls = [url];
      frame.removeAttribute("src");
      frame.srcdoc = "";
      frame.classList.add("is-hidden");
      if (image) {
        image.src = url;
        image.classList.add("is-visible");
      }
      return;
    } catch (error) {
      fallback.textContent = error.message || t("filePreviewFailed");
      fallback.classList.add("is-visible");
      return;
    }
  }

  renderFilePreviewPages(uploadId, { page_count: 1, visible_pages: [1] }, 1);
  try {
    const response = await fetch(`/files/uploads/${encodeURIComponent(uploadId)}/content`, {
      headers: state.token ? { Authorization: `Bearer ${state.token}` } : {},
    });
    if (!response.ok) throw new Error(response.statusText || t("filePreviewFailed"));
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    state.filePreviewUrl = url;
    if (image) {
      image.removeAttribute("src");
      image.classList.remove("is-visible");
    }
    frame.srcdoc = "";
    frame.classList.remove("is-hidden");
    frame.src = url;
  } catch (error) {
    frame.removeAttribute("src");
    frame.srcdoc = "";
    fallback.textContent = error.message || t("filePreviewFailed");
    fallback.classList.add("is-visible");
  }
}

function closeFilePreview(resetText = true) {
  const frame = $("#filePreviewFrame");
  const image = $("#filePreviewImage");
  const fallback = $("#filePreviewFallback");
  const pages = $("#filePreviewPages");
  revokeFilePreviewUrls();
  if (frame) {
    frame.removeAttribute("src");
    frame.srcdoc = "";
    frame.classList.add("is-hidden");
  }
  if (image) {
    image.removeAttribute("src");
    image.classList.remove("is-visible");
  }
  if (fallback) {
    fallback.textContent = "";
    fallback.classList.remove("is-visible");
  }
  if (pages) {
    pages.hidden = true;
    pages.innerHTML = "";
  }
  if (resetText) {
    $("#caseFilePreviewDrawer")?.classList.add("is-hidden");
    $("#filePreviewPanel")?.classList.remove("is-open");
    setText("#fileLookupStatus", "Uploaded file registry");
    setText("#filePreviewTitle", t("noFileSelected"));
    setText("#filePreviewMeta", t("selectFileToPreview"));
  }
}

function fileUploadMeta(upload) {
  const linked = [upload.linked_fir_number, upload.linked_district].filter(Boolean).join(" / ");
  const parts = [
    linked || labelValue(upload.upload_type),
    prettyBytes(upload.size_bytes),
    upload.extraction_status ? labelValue(upload.extraction_status) : "",
  ];
  return parts.filter(Boolean).join(" | ");
}

async function loadTrends() {
  try {
    state.trends = await api("/analytics/trends");
    renderTrends();
  } catch (error) {
    renderPermission("#trendBars", error.message);
  }
}

async function loadPatterns() {
  try {
    state.patterns = await api("/analytics/patterns");
    renderPatterns();
  } catch (error) {
    renderPermission("#patternClusters", error.message);
    renderPermission("#patternBars", error.message);
    renderPermission("#patternQuality", error.message);
  }
}

async function loadAdvancedCrime() {
  try {
    state.advancedCrime = await api("/analytics/advanced-crime");
    renderOverview();
    renderPatterns();
    renderMapInsights();
    renderNetwork();
    renderCrimeMap();
    updateCommandHeader();
  } catch (error) {
    state.advancedCrime = null;
    renderPermission("#patternQuality", error.message);
  }
}

async function loadNetwork() {
  try {
    const params = new URLSearchParams();
    if (state.networkView.focus.trim()) {
      params.set("focus", state.networkView.focus.trim());
      params.set("focus_type", state.networkView.focusType || "auto");
      params.set("hops", "4");
    }
    state.network = await api(`/analytics/network${params.toString() ? `?${params}` : ""}`);
    renderNetwork();
    updateCommandHeader();
  } catch (error) {
    const container = $("#networkCy");
    if (container) {
      container.innerHTML = `<div class="network-empty-state">${escapeHtml(error.message)}</div>`;
    }
    setText("#networkProgressiveNote", error.message);
  }
}

async function loadSociological() {
  try {
    state.socio = await api("/analytics/sociological");
    renderSociological();
  } catch (error) {
    renderPermission("#socioList", error.message);
  }
}

async function loadFinancial() {
  try {
    state.financial = await api("/financial/analysis");
    renderFinancial();
    updateCommandHeader();
  } catch (error) {
    renderPermission("#financialFindings", error.message);
  }
}

async function loadForecast() {
  try {
    state.forecast = await api("/forecast/hotspots");
    renderForecast();
    renderOverview();
    updateCommandHeader();
  } catch (error) {
    renderPermission("#forecastBars", error.message);
    renderPermission("#hotspotList", error.message);
  }
}

async function loadAudit() {
  try {
    const [integrity, logs] = await Promise.all([
      api("/audit/integrity"),
      api("/audit/logs?limit=12"),
    ]);
    renderAudit(integrity, logs);
  } catch (error) {
    renderPermission("#auditIntegrity", error.message);
    renderPermission("#auditLogs", error.message);
  }
}

function renderOverview() {
  const cases = state.cases || [];
  const open = cases.filter((item) => item.status === "open").length;
  const restricted = cases.filter((item) => item.sensitivity === "restricted").length;
  const findings = state.financial?.findings?.length || 0;
  const hotspots = state.forecast?.hotspots?.length || 0;
  const importedIncidents = state.advancedCrime?.imported_count || 0;
  const riskAreas = state.advancedCrime?.risk_areas?.length || 0;
  $("#kpiGrid").innerHTML = [
    metric(t("cases"), cases.length, t("authorizedRecords")),
    metric(t("openCases"), open, t("currentWorkload")),
    metric(t("mlIncidents"), importedIncidents, t("integratedDataset")),
    metric(t("riskAreas"), riskAreas || hotspots, t("forecastHotspots")),
  ].join("");
  renderTopViewMetrics();
  renderHotspots();
}

function renderTopViewMetrics() {
  const cases = state.cases || [];
  const districts = new Set(cases.map((item) => item.district)).size;
  const restricted = cases.filter((item) => item.sensitivity === "restricted").length;
  const findings = state.financial?.findings?.length || 0;
  const importedIncidents = state.advancedCrime?.imported_count || 0;
  $("#topViewMetrics").innerHTML = [
    topChip(t("cases"), cases.length),
    topChip(t("mlIncidents"), importedIncidents),
    topChip(t("districts"), districts),
    topChip(t("restricted"), restricted),
    topChip(t("findings"), findings),
    topChip(t("map"), state.mapProvider === "google" ? "Google" : "Leaflet"),
  ].join("");
  updateCommandHeader();
}

function renderModules() {
  $("#moduleGrid").innerHTML = state.modules
    .map(
      (module) => `
        <article class="module-card">
          <span class="badge">${escapeHtml(moduleStatusLabel(module.status))}</span>
          <h3>${escapeHtml(moduleLabel(module))}</h3>
          <p>${escapeHtml(module.endpoint)}</p>
        </article>
      `,
    )
    .join("");
}

function renderFramework() {
  const framework = state.framework;
  if (!framework) {
    setText("#frameworkMission", t("checking"));
    $("#frameworkTasks").innerHTML = "";
    $("#frameworkGrid").innerHTML = "";
    $("#commandTaskLaunch").innerHTML = "";
    return;
  }
  setText("#frameworkMission", framework.mission);
  renderTaskLaunch("#frameworkTasks", framework.core_tasks || []);
  renderTaskLaunch("#commandTaskLaunch", framework.core_tasks || []);
  $("#frameworkGrid").innerHTML = (framework.solution_framework || [])
    .map((item, index) => `
      <article class="framework-card">
        <span class="framework-index">${String(index + 1).padStart(2, "0")}</span>
        <div>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.objective)}</p>
        </div>
        <ul>
          ${(item.capabilities || []).map((capability) => `<li>${escapeHtml(capability)}</li>`).join("")}
        </ul>
        <div class="endpoint-row">
          ${(item.endpoints || []).map((endpoint) => `<span>${escapeHtml(endpoint)}</span>`).join("")}
        </div>
      </article>
    `)
    .join("");
  bindTaskLaunchers();
}

function renderTaskLaunch(selector, tasks) {
  const target = $(selector);
  if (!target) return;
  target.innerHTML = tasks
    .map((task) => `
      <button type="button" class="task-launch" data-task-id="${escapeHtml(task.id)}">
        <strong>${escapeHtml(task.label)}</strong>
        <span>${escapeHtml(t("launchQuery"))}</span>
      </button>
    `)
    .join("");
}

function bindTaskLaunchers() {
  $$("[data-task-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const task = state.framework?.core_tasks?.find((item) => item.id === button.dataset.taskId);
      if (!task) return;
      launchTaskPrompt(task.prompt);
    });
  });
}

function uploadsForCase(item) {
  const firNumber = String(item?.fir_number || "").toLowerCase();
  return (state.fileUploads || [])
    .filter((upload) => {
      if (!upload.preview_supported) return false;
      if (upload.case_id && item?.id && upload.case_id === item.id) return true;
      return firNumber && String(upload.linked_fir_number || "").toLowerCase() === firNumber;
    })
    .sort((a, b) => new Date(b.uploaded_at || 0) - new Date(a.uploaded_at || 0));
}

function casePreviewButton(item) {
  const upload = uploadsForCase(item)[0];
  if (!upload) {
    return `
      <button type="button" class="case-preview-button is-disabled" disabled title="No linked FIR/case file">
        <i data-lucide="file-search"></i><span>No file</span>
      </button>
    `;
  }
  return `
    <button type="button" class="case-preview-button" data-case-file-preview="${escapeHtml(upload.id)}" title="Preview linked file">
      <i data-lucide="eye"></i><span>Preview</span>
    </button>
  `;
}

function renderCases() {
  const rows = state.cases
    .map(
      (item) => `
        <tr>
          <td><strong>${escapeHtml(item.fir_number)}</strong><p>${escapeHtml(item.summary)}</p></td>
          <td class="case-preview-cell">${casePreviewButton(item)}</td>
          <td>${escapeHtml(item.district)}</td>
          <td>${statusBadge(item.status)}</td>
          <td>${escapeHtml(item.suspect_name)}</td>
          <td>${statusBadge(item.sensitivity)}</td>
          <td>
            <div class="row-actions">
              <button class="icon-button" title="Select for support" aria-label="Select for support" data-case-select="${item.id}"><i data-lucide="clipboard-check"></i></button>
              <button class="icon-button" title="Mark under review" aria-label="Mark under review" data-case-status="${item.id}:under_review"><i data-lucide="clock-3"></i></button>
              <button class="icon-button" title="Close case" aria-label="Close case" data-case-status="${item.id}:closed"><i data-lucide="check"></i></button>
            </div>
          </td>
        </tr>
      `,
    )
    .join("");
  $("#caseRows").innerHTML = rows || `<tr><td colspan="7">${escapeHtml(t("noCasesForRole"))}</td></tr>`;
  $$("[data-case-file-preview]").forEach((button) => {
    button.addEventListener("click", () => previewFileUpload(button.dataset.caseFilePreview));
  });
  $$("[data-case-select]").forEach((button) => {
    button.addEventListener("click", () => {
      $("#caseSelect").value = button.dataset.caseSelect;
      setPanel("support");
    });
  });
  $$("[data-case-status]").forEach((button) => {
    button.addEventListener("click", () => {
      const [caseId, status] = button.dataset.caseStatus.split(":");
      updateCaseStatus(caseId, status);
    });
  });
  iconRefresh();
  renderCrimeMap();
}

async function updateCaseStatus(caseId, status) {
  try {
    await api(`/cases/${caseId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    await loadCases();
    await loadTrends();
  } catch (error) {
    alert(error.message);
  }
}

function renderCaseSelect() {
  $("#caseSelect").innerHTML = state.cases
    .map((item) => `<option value="${item.id}">${escapeHtml(item.fir_number)} - ${escapeHtml(item.district)}</option>`)
    .join("");
  const uploadSelect = $("#uploadCaseId");
  if (uploadSelect) {
    uploadSelect.innerHTML = [
      `<option value="">${escapeHtml(t("noLinkedCase"))}</option>`,
      ...state.cases.map((item) => `<option value="${item.id}">${escapeHtml(item.fir_number)} - ${escapeHtml(item.district)}</option>`),
    ].join("");
    renderUploadControls();
  }
}

function renderTrends() {
  const trend = state.trends;
  if (!trend) return;
  $("#trendBars").innerHTML = [
    ...barRows(t("district"), trend.by_district),
    ...barRows(t("status"), trend.by_status),
    ...barRows(t("sensitivity"), trend.by_sensitivity),
    ...barRows("MO", trend.by_modus_operandi || []),
  ].join("");
}

function renderPatterns() {
  if (!state.patterns) return;
  const patterns = state.patterns;
  const advanced = state.advancedCrime;
  const alerts = advanced?.emerging_trend_alerts || [];
  const risks = advanced?.risk_areas || [];
  const anomalies = advanced?.anomalies || [];
  $("#patternClusters").innerHTML = patterns.clusters?.length
    ? patterns.clusters
        .map((cluster) =>
          listItem(
            cluster.key,
            `${cluster.count} case(s) / FIR: ${cluster.fir_numbers.join(", ")} / ${Math.round(cluster.confidence * 100)}%`,
          ),
        )
        .join("")
    : alerts.length
      ? alerts
          .slice(0, 12)
          .map((item) => listItem(`${item.district} / ${item.crime_type}`, item.explanation, `severity-${item.severity}`))
          .join("")
      : listItem(t("noClusters"), t("noClustersBody"));
  $("#patternBars").innerHTML = [
    ...barRows(t("caseType"), patterns.by_case_type || []),
    ...barRows("MO", patterns.by_modus_operandi || []),
    ...barRows(t("month"), patterns.by_month || []),
    ...barRows(t("event"), patterns.event_trends || []),
  ].join("") || `<p class="muted-copy">${escapeHtml(t("noPatternBars"))}</p>`;
  const riskItems = risks
    .slice(0, 10)
    .map((item) =>
      listItem(
        `${item.district} / ${item.crime_type}`,
        `${t("riskScore")}: ${item.score} / ${labelValue(item.risk_level)}. ${item.drivers.join(", ")}`,
        `severity-${item.risk_level}`,
      ),
    );
  const anomalyItems = anomalies
    .slice(0, 8)
    .map((item) => listItem(t("anomaly"), item.explanation, "warning-card"));
  const qualityItems = [
    ...(patterns.data_quality || []),
    ...(advanced?.data_quality || []),
  ].map((item) => listItem(t("dataQuality"), item));
  $("#patternQuality").innerHTML = [...riskItems, ...anomalyItems, ...qualityItems].join("")
    || listItem(t("dataQuality"), t("fieldCoverageGood"));
}

function renderSociological() {
  if (!state.socio) return;
  const demographics = Object.entries(state.socio.demographic_mix || {})
    .flatMap(([group, buckets]) => (buckets || []).map((bucket) => listItem(`${labelValue(group)} / ${bucket.key}`, `${bucket.count}`)));
  const social = (state.socio.social_indicators || []).map((item) => listItem(t("socialIndicator"), `${item.key}: ${item.count}`));
  const correlations = (state.socio.correlations || []).map((item) => listItem(t("correlation"), item));
  const observations = state.socio.observations.map((item) => listItem(t("observation"), item));
  $("#socioList").innerHTML = [...observations, ...demographics, ...social, ...correlations].join("");
}

function renderNetwork() {
  const container = $("#networkCy");
  const canvas = $("#networkCanvasFallback");
  const graph = state.network;
  renderNetworkFocusAlert(graph);
  if (!graph || !graph.nodes?.length) {
    if (state.networkCy) {
      state.networkCy.destroy();
      state.networkCy = null;
    }
    if ($("#networkMetricsBar")) $("#networkMetricsBar").innerHTML = "";
    if ($("#networkCommunityList")) $("#networkCommunityList").innerHTML = `<p class="muted-copy">No cells detected.</p>`;
    if ($("#networkWatchList")) $("#networkWatchList").innerHTML = `<p class="muted-copy">No high-value nodes detected.</p>`;
    if ($("#networkAnomalyList")) $("#networkAnomalyList").innerHTML = `<p class="muted-copy">No financial anomalies detected.</p>`;
    setText("#networkProgressiveNote", graph?.focus?.active ? "No focused graph found for this account/FIR/person." : "No graph data available.");
    if (container) container.innerHTML = `<div class="network-empty-state">No graph data available.</div>`;
    closeNetworkPanel();
    $("#networkDetail").innerHTML = `
      <button class="icon-button network-panel-close" type="button" id="networkPanelCloseEmpty" title="Close node panel" aria-label="Close node panel"><i data-lucide="x"></i></button>
      <p class="eyebrow">Selection panel</p>
      <h3>No network data</h3>
      <p class="muted-copy">No accessible suspect, case, or transaction records are available for this role.</p>
    `;
    lucide.createIcons();
    return;
  }
  if (!$("#network")?.classList.contains("is-active")) return;
  const prepared = prepareNetworkForWorkbench(graph);
  state.networkPrepared = prepared;
  renderNetworkMetrics(prepared);
  renderNetworkSideLists(prepared);
  renderNetworkCommunityControls(prepared);
  updateNetworkTimeLabel(prepared);
  if (!prepared.nodes.length) {
    if (state.networkCy) {
      state.networkCy.destroy();
      state.networkCy = null;
    }
    if (container) container.innerHTML = `<div class="network-empty-state">No nodes match the current mode, community, search, or time filter.</div>`;
    closeNetworkPanel();
    return;
  }
  if (state.selectedNetworkNodeId && !prepared.nodes.some((node) => node.id === state.selectedNetworkNodeId)) {
    state.selectedNetworkNodeId = null;
    closeNetworkPanel();
  }
  setText("#networkProgressiveNote", progressiveNetworkNote(prepared));
  if (window.cytoscape && container) {
    renderCytoscapeNetwork(prepared, container, canvas);
  } else {
    renderCanvasNetwork(prepared, canvas);
  }
  if (state.selectedNetworkNodeId) {
    renderNetworkDetails(state.selectedNetworkNodeId, graph);
  }
  lucide.createIcons();
}

function renderNetworkFocusAlert(graph) {
  const panel = $("#networkFocusAlert");
  if (!panel) return;
  const focus = graph?.focus || {};
  if (!focus.active) {
    panel.className = "network-focus-alert";
    panel.innerHTML = `
      <span><i data-lucide="info"></i> Full network mode</span>
      <strong>Enter a FIR, case ID, account number, IFSC, or account-holder name to isolate a specific investigation graph.</strong>
    `;
    return;
  }
  const alerts = focus.alerts || [];
  const severity = alerts.some((item) => item.severity === "high") ? "high" : alerts.some((item) => item.severity === "medium") ? "medium" : "low";
  panel.className = `network-focus-alert is-active severity-${severity}`;
  const linkedFirs = (focus.linked_firs || []).slice(0, 8).join(", ");
  panel.innerHTML = `
    <span><i data-lucide="${severity === "high" ? "shield-alert" : "radar"}"></i> Focused trace: ${escapeHtml(focus.query || "")}</span>
    <strong>${escapeHtml(formatCount(focus.transaction_count || 0))} transaction(s), ${escapeHtml(formatCount(focus.case_count || 0))} FIR link(s), ${escapeHtml(formatCount((focus.seed_accounts || []).length))} account node(s).</strong>
    ${linkedFirs ? `<em>Linked FIRs: ${escapeHtml(linkedFirs)}</em>` : ""}
    <div>
      ${alerts.slice(0, 4).map((item) => `<p><b>${escapeHtml(item.title)}</b> ${escapeHtml(item.message)}</p>`).join("")}
    </div>
  `;
}

function prepareNetworkForWorkbench(graph) {
  const base = getNetworkAnalysis(graph);
  const search = state.networkView.search.trim().toLowerCase();
  const mode = state.networkView.mode;
  const community = state.networkView.community;
  const cutoff = networkTimeCutoff(base);
  const allowedByTime = new Set();
  const filteredLinks = base.links.filter((link) => {
    if (cutoff && link._date && link._date > cutoff) return false;
    if (mode === "money" && !isMoneyRelationship(link.relationship)) return false;
    return true;
  });
  filteredLinks.forEach((link) => {
    allowedByTime.add(link.source);
    allowedByTime.add(link.target);
  });
  let nodes = base.nodes.filter((node) => {
    if (mode === "money" && !["financial_account", "bank", "ifsc", "branch", "bank_manager", "dead_end", "suspect", "case"].includes(node.type)) {
      return false;
    }
    if (community !== "all" && String(node._community) !== String(community)) return false;
    if (search && !networkNodeSearchText(node).includes(search)) return false;
    if (mode === "money" && !allowedByTime.has(node.id) && !["financial_account", "bank", "ifsc", "branch", "bank_manager", "dead_end"].includes(node.type)) {
      return false;
    }
    return true;
  });
  nodes = nodes
    .sort((a, b) => b._importance - a._importance || String(a.label).localeCompare(String(b.label)))
    .slice(0, state.networkView.renderLimit);
  const nodeIds = new Set(nodes.map((node) => node.id));
  let links = filteredLinks.filter((link) => nodeIds.has(link.source) && nodeIds.has(link.target));
  if (mode === "path" && state.networkView.pathStart && state.networkView.pathEnd) {
    const pathLinks = shortestNetworkPath(state.networkView.pathStart, state.networkView.pathEnd, links);
    const pathEdgeIds = new Set(pathLinks.map(edgeKey));
    links = links.map((link) => ({ ...link, _path: pathEdgeIds.has(edgeKey(link)), _dim: !pathEdgeIds.has(edgeKey(link)) }));
    const pathNodeIds = new Set(pathLinks.flatMap((link) => [link.source, link.target]));
    nodes = nodes.map((node) => ({ ...node, _path: pathNodeIds.has(node.id), _dim: pathNodeIds.size ? !pathNodeIds.has(node.id) : false }));
  }
  return { ...base, nodes, links, filteredNodeCount: nodes.length, filteredLinkCount: links.length };
}

function getNetworkAnalysis(graph) {
  const signature = `${graph.generated_at || ""}:${graph.nodes?.length || 0}:${graph.links?.length || 0}`;
  if (state.networkAnalysisCache?.signature === signature && state.networkAnalysisCache?.base) {
    return state.networkAnalysisCache.base;
  }
  const allNodes = (graph.nodes || []).slice(0, Math.max(10000, state.networkView.renderLimit));
  const nodeIds = new Set(allNodes.map((node) => node.id));
  const allLinks = (graph.links || []).filter((link) => nodeIds.has(link.source) && nodeIds.has(link.target));
  const degreeMap = calculateWeightedDegrees(allNodes, allLinks);
  const communities = detectCommunitiesLouvain(allNodes, allLinks);
  const pageRank = calculatePageRank(allNodes, allLinks);
  const betweenness = calculateBetweennessCentrality(allNodes, allLinks);
  const maxDegree = Math.max(1, ...Array.from(degreeMap.values()));
  const nodes = allNodes.map((node) => {
    const degree = degreeMap.get(node.id) || 0;
    const centrality = degree / maxDegree;
    const risk = estimateNodeRisk(node, centrality, pageRank.get(node.id) || 0, betweenness.get(node.id) || 0);
    const community = communities.get(node.id) ?? 0;
    return {
      ...node,
      _degree: degree,
      _centrality: centrality,
      _pagerank: pageRank.get(node.id) || 0,
      _betweenness: betweenness.get(node.id) || 0,
      _community: community,
      _risk: risk,
      _size: Math.max(9, Math.min(46, 10 + centrality * 34 + Math.log1p(node.case_count || 0) * 3)),
      _color: riskColor(risk),
      _importance: risk + centrality * 50 + (pageRank.get(node.id) || 0) * 1000 + (betweenness.get(node.id) || 0) * 400,
    };
  });
  const nodeMap = new Map(nodes.map((node) => [node.id, node]));
  const links = allLinks.map((link, index) => ({
    ...link,
    id: link.id || `e:${index}:${link.source}:${link.target}:${link.relationship}`,
    _date: networkLinkDate(link, nodeMap),
    _money: isMoneyRelationship(link.relationship),
    _circular: false,
    _weight: Math.max(1, Number(link.weight || 1)),
  }));
  const circularEdges = detectCircularMoneyFlows(links);
  links.forEach((link) => {
    link._circular = circularEdges.has(edgeKey(link));
  });
  const communitiesSummary = summarizeCommunities(nodes, links);
  const kingpins = nodes.filter((node) => ["suspect", "financial_account"].includes(node.type)).sort((a, b) => b._pagerank - a._pagerank).slice(0, 8);
  const brokers = nodes.filter((node) => node._betweenness > 0).sort((a, b) => b._betweenness - a._betweenness).slice(0, 8);
  const suspiciousChains = detectSuspiciousAccountChains(nodes, links);
  const base = {
    signature,
    nodes,
    links,
    nodeMap,
    communities: communitiesSummary,
    kingpins,
    brokers,
    suspiciousChains,
    circularFlows: links.filter((link) => link._circular),
    metrics: {
      totalNodes: nodes.length,
      totalLinks: links.length,
      communities: communitiesSummary.length,
      kingpins: kingpins.length,
      brokers: brokers.length,
      suspiciousChains: suspiciousChains.length,
      circularFlows: links.filter((link) => link._circular).length,
      density: graphDensity(nodes.length, links.length),
    },
  };
  state.networkAnalysisCache = { signature, base };
  return base;
}

function renderCytoscapeNetwork(prepared, container, canvas) {
  if (canvas) canvas.classList.add("is-hidden");
  container.classList.remove("is-hidden");
  if (state.networkCy) {
    state.networkCy.destroy();
    state.networkCy = null;
  }
  const elements = [
    ...prepared.nodes.map((node) => {
      const photo = networkNodePhoto(node);
      return {
        group: "nodes",
        data: {
          id: node.id,
          label: networkNodeDisplayLabel(node),
          displayLabel: node.id === state.selectedNetworkNodeId ? networkNodeDisplayLabel(node) : "",
          type: node.type,
          risk: node._risk,
          community: node._community,
          size: node._size,
          color: node._color,
          border: communityColor(node._community),
          photo,
        },
        classes: [
          photo ? "has-photo" : "",
          node._path ? "path-node" : "",
          node._dim ? "is-dim" : "",
          node.id === state.selectedNetworkNodeId ? "selected-node" : "",
        ].join(" "),
      };
    }),
    ...prepared.links.map((link) => ({
      group: "edges",
      data: {
        id: link.id,
        source: link.source,
        target: link.target,
        label: relationshipLabel(link.relationship),
        width: Math.min(8, 1 + Math.log1p(link._weight || link.weight || 1) * 1.8),
      },
      classes: [
        link._money ? "money-edge" : "case-edge",
        link._circular ? "circular-edge" : "",
        link._path ? "path-edge" : "",
        link._dim ? "is-dim" : "",
      ].join(" "),
    })),
  ];
  const layoutName = prepared.nodes.length <= 160 && prepared.links.length <= 420 ? "cose" : "preset";
  const presetPositions = layoutName === "preset" ? deterministicNetworkPositions(prepared.nodes, prepared.links) : {};
  elements.forEach((element) => {
    if (element.group === "nodes" && presetPositions[element.data.id]) {
      element.position = presetPositions[element.data.id];
    }
  });
  const cy = window.cytoscape({
    container,
    elements,
    boxSelectionEnabled: false,
    autoungrabify: prepared.nodes.length > 1200,
    textureOnViewport: true,
    hideEdgesOnViewport: prepared.nodes.length > 1800,
    motionBlur: prepared.nodes.length > 450,
    wheelSensitivity: 0.18,
    minZoom: 0.08,
    maxZoom: 4,
    style: cytoscapeNetworkStyle(),
    layout: layoutName === "cose"
      ? {
          name: "cose",
          animate: false,
          fit: true,
          padding: 38,
          nodeRepulsion: 580000,
          idealEdgeLength: 112,
          edgeElasticity: 90,
          gravity: 0.18,
          numIter: prepared.nodes.length > 300 ? 750 : 1100,
        }
      : { name: "preset", fit: true, padding: 42 },
  });
  state.networkCy = cy;
  cy.on("mouseover", "node", (event) => {
    const node = event.target;
    node.data("displayLabel", node.data("label"));
    showNetworkHoverLabel(node.data("label"), event.originalEvent);
    highlightNeighborhood(node.id());
  });
  cy.on("mouseout", "node", (event) => {
    const node = event.target;
    if (node.id() !== state.selectedNetworkNodeId) node.data("displayLabel", "");
    hideNetworkHoverLabel();
    clearNeighborhoodHighlight();
  });
  cy.on("tap", "node", (event) => selectNetworkNode(event.target.id(), state.network));
  cy.on("tap", (event) => {
    if (event.target === cy) closeNetworkPanel();
  });
  requestAnimationFrame(() => cy.resize());
}

function cytoscapeNetworkStyle() {
  return [
    {
      selector: "node",
      style: {
        width: "data(size)",
        height: "data(size)",
        "background-color": "data(color)",
        "border-color": "data(border)",
        "border-width": 2,
        "background-blacken": -0.06,
        "shadow-blur": 18,
        "shadow-color": "data(color)",
        "shadow-opacity": 0.22,
        "shadow-offset-x": 0,
        "shadow-offset-y": 0,
        label: "data(displayLabel)",
        color: "#f8fafc",
        "font-size": 11,
        "font-weight": 800,
        "text-outline-color": "#0a0f1f",
        "text-outline-width": 4,
        "text-valign": "bottom",
        "text-margin-y": 10,
        "overlay-opacity": 0,
        "transition-property": "opacity, border-width, width, height, shadow-opacity",
        "transition-duration": "160ms",
      },
    },
    {
      selector: "node.has-photo",
      style: {
        "background-image": "data(photo)",
        "background-fit": "cover cover",
        "background-clip": "node",
        "background-width": "100%",
        "background-height": "100%",
      },
    },
    { selector: "node[type = 'case']", style: { shape: "round-rectangle" } },
    { selector: "node[type = 'financial_account']", style: { shape: "diamond" } },
    { selector: "node[type = 'bank'], node[type = 'ifsc'], node[type = 'branch']", style: { shape: "hexagon" } },
    { selector: "node[type = 'dead_end']", style: { shape: "vee", "background-color": "#64748b" } },
    { selector: "node[type = 'bank_manager']", style: { shape: "tag" } },
    {
      selector: "edge",
      style: {
        width: "data(width)",
        "line-color": "rgba(71, 85, 105, 0.45)",
        "target-arrow-color": "rgba(71, 85, 105, 0.62)",
        "target-arrow-shape": "triangle",
        "arrow-scale": 0.72,
        "curve-style": "unbundled-bezier",
        "control-point-distances": "28 -28",
        "control-point-weights": "0.35 0.65",
        opacity: 0.52,
        "overlay-opacity": 0,
        "transition-property": "opacity, line-color, width",
        "transition-duration": "140ms",
      },
    },
    { selector: "edge.money-edge", style: { "line-color": "#00b894", "target-arrow-color": "#00b894", opacity: 0.82, width: "mapData(width, 1, 8, 2, 9)" } },
    { selector: "edge.circular-edge", style: { "line-color": "#f59e0b", "target-arrow-color": "#f59e0b", "line-style": "dashed", opacity: 0.96 } },
    { selector: ".path-edge", style: { "line-color": "#1a73e8", "target-arrow-color": "#1a73e8", width: 6, opacity: 1, "z-index": 20 } },
    { selector: ".path-node", style: { "border-color": "#1a73e8", "border-width": 5, "shadow-opacity": 0.5 } },
    { selector: ".selected-node", style: { "border-color": "#ffffff", "border-width": 6, label: "data(label)", "shadow-opacity": 0.62, "z-index": 30 } },
    { selector: ".is-dim", style: { opacity: 0.12 } },
    { selector: ".is-neighborhood-dim", style: { opacity: 0.12 } },
    { selector: ".is-neighborhood-focus", style: { opacity: 1, "border-width": 5, "shadow-opacity": 0.48, "z-index": 25 } },
  ];
}

function renderCanvasNetwork(prepared, canvas) {
  const container = $("#networkCy");
  if (container) {
    container.classList.add("is-hidden");
    container.innerHTML = "";
  }
  if (!canvas) return;
  canvas.classList.remove("is-hidden");
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = Math.max(640, Math.floor(rect.width * window.devicePixelRatio));
  canvas.height = Math.max(460, Math.floor(rect.height * window.devicePixelRatio));
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;
  const ctx = canvas.getContext("2d");
  ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
  const positions = deterministicNetworkPositions(prepared.nodes, prepared.links, rect.width, rect.height);
  ctx.clearRect(0, 0, rect.width, rect.height);
  ctx.lineCap = "round";
  prepared.links.forEach((link) => {
    const source = positions[link.source];
    const target = positions[link.target];
    if (!source || !target) return;
    const midX = (source.x + target.x) / 2;
    const midY = (source.y + target.y) / 2 - 24;
    ctx.beginPath();
    ctx.moveTo(source.x, source.y);
    ctx.quadraticCurveTo(midX, midY, target.x, target.y);
    ctx.strokeStyle = link._path ? "#4ea8ff" : link._circular ? "#f7b955" : link._money ? "#00d4aa" : "rgba(148,163,184,.36)";
    ctx.globalAlpha = link._dim ? 0.16 : 0.78;
    ctx.lineWidth = Math.min(7, 1 + Math.log1p(link._weight || link.weight || 1) * 1.7);
    ctx.stroke();
  });
  prepared.nodes.forEach((node) => {
    const point = positions[node.id];
    if (!point) return;
    const size = Math.max(7, node._size / 2);
    ctx.globalAlpha = node._dim ? 0.18 : 1;
    ctx.beginPath();
    ctx.arc(point.x, point.y, size, 0, Math.PI * 2);
    ctx.fillStyle = node._color;
    ctx.fill();
    ctx.lineWidth = node.id === state.selectedNetworkNodeId ? 4 : 2;
    ctx.strokeStyle = node.id === state.selectedNetworkNodeId ? "#f8fafc" : communityColor(node._community);
    ctx.stroke();
  });
  canvas.onclick = (event) => {
    const bounds = canvas.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;
    const nearest = prepared.nodes
      .map((node) => ({ node, point: positions[node.id] }))
      .filter((item) => item.point)
      .map((item) => ({ ...item, distance: Math.hypot(item.point.x - x, item.point.y - y) }))
      .sort((a, b) => a.distance - b.distance)[0];
    if (nearest && nearest.distance < Math.max(18, nearest.node._size)) {
      selectNetworkNode(nearest.node.id, state.network);
    }
  };
}

function deterministicNetworkPositions(nodes, links, width = 1180, height = 720) {
  const communities = new Map();
  nodes.forEach((node) => {
    const key = String(node._community ?? 0);
    if (!communities.has(key)) communities.set(key, []);
    communities.get(key).push(node);
  });
  const centerX = width / 2;
  const centerY = height / 2;
  const communityKeys = Array.from(communities.keys()).sort((a, b) => Number(a) - Number(b));
  const outerRadius = Math.max(180, Math.min(width, height) * 0.34);
  const positions = {};
  communityKeys.forEach((community, communityIndex) => {
    const angle = (Math.PI * 2 * communityIndex) / Math.max(1, communityKeys.length);
    const clusterX = centerX + Math.cos(angle) * outerRadius * 0.62;
    const clusterY = centerY + Math.sin(angle) * outerRadius * 0.46;
    const group = communities.get(community).sort((a, b) => b._importance - a._importance);
    const radius = Math.max(42, Math.sqrt(group.length) * 18);
    group.forEach((node, index) => {
      const nodeAngle = (index * 2.399963229728653) % (Math.PI * 2);
      const nodeRadius = radius * Math.sqrt((index + 1) / Math.max(1, group.length));
      positions[node.id] = {
        x: clusterX + Math.cos(nodeAngle) * nodeRadius,
        y: clusterY + Math.sin(nodeAngle) * nodeRadius,
      };
    });
  });
  return positions;
}

function renderNetworkMetrics(prepared) {
  const metrics = prepared.metrics;
  const items = [
    ["Nodes", prepared.filteredNodeCount, `${metrics.totalNodes} total`],
    ["Connections", prepared.filteredLinkCount, `${metrics.totalLinks} total`],
    ["Cells", metrics.communities, "Louvain detected"],
    ["Kingpins", metrics.kingpins, "PageRank"],
    ["Brokers", metrics.brokers, "Betweenness"],
    ["Circular flows", metrics.circularFlows, "money loop"],
    ["Density", metrics.density, "graph"],
  ];
  $("#networkMetricsBar").innerHTML = items.map(([label, value, note]) => `
    <div class="network-metric">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(formatCount(value))}</strong>
      <small>${escapeHtml(note)}</small>
    </div>
  `).join("");
}

function renderNetworkSideLists(prepared) {
  $("#networkCommunityList").innerHTML = prepared.communities.slice(0, 8).map((community) => `
    <button type="button" data-network-community="${escapeAttr(community.id)}">
      <i style="background:${communityColor(community.id)}"></i>
      <span>Cell ${escapeHtml(String(community.id))}</span>
      <b>${escapeHtml(formatCount(community.nodeCount))}</b>
    </button>
  `).join("") || `<p class="muted-copy">No cells detected.</p>`;
  $("#networkWatchList").innerHTML = [
    ...prepared.kingpins.slice(0, 4).map((node) => watchItem("Kingpin", node, "PageRank")),
    ...prepared.brokers.slice(0, 4).map((node) => watchItem("Broker", node, "Betweenness")),
  ].join("") || `<p class="muted-copy">No high-value nodes detected.</p>`;
  $("#networkAnomalyList").innerHTML = [
    ...prepared.suspiciousChains.slice(0, 4).map((chain) => anomalyItem("Suspicious chain", chain.labels.join(" -> "))),
    ...prepared.circularFlows.slice(0, 4).map((link) => anomalyItem("Circular money flow", `${nodeLabel(link.source, prepared)} -> ${nodeLabel(link.target, prepared)}`)),
  ].join("") || `<p class="muted-copy">No financial anomalies detected.</p>`;
  $$("[data-network-community]").forEach((button) => {
    button.addEventListener("click", () => {
      state.networkView.community = button.dataset.networkCommunity || "all";
      $("#networkCommunitySelect").value = state.networkView.community;
      renderNetwork();
    });
  });
  $$("[data-network-watch]").forEach((button) => {
    button.addEventListener("click", () => {
      selectNetworkNode(button.dataset.networkWatch, state.network);
      const cyNode = state.networkCy?.getElementById(button.dataset.networkWatch);
      if (cyNode?.length) state.networkCy.animate({ center: { eles: cyNode }, zoom: Math.max(1.35, state.networkCy.zoom()) }, { duration: 360 });
    });
  });
}

function watchItem(label, node, basis) {
  return `
    <button type="button" data-network-watch="${escapeAttr(node.id)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(shorten(node.label, 24))}</strong>
      <small>${escapeHtml(basis)} / risk ${Math.round(node._risk)}</small>
    </button>
  `;
}

function anomalyItem(label, value) {
  return `
    <article>
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(shorten(value, 54))}</strong>
    </article>
  `;
}

function renderNetworkCommunityControls(prepared) {
  const select = $("#networkCommunitySelect");
  if (!select) return;
  const current = state.networkView.community;
  select.innerHTML = [
    `<option value="all">All cells</option>`,
    ...prepared.communities.map((community) => `<option value="${escapeAttr(community.id)}">Cell ${escapeHtml(String(community.id))} / ${escapeHtml(formatCount(community.nodeCount))} nodes</option>`),
  ].join("");
  select.value = [...select.options].some((option) => option.value === current) ? current : "all";
  if (select.value !== current) state.networkView.community = select.value;
}

function handleNetworkSearch(event) {
  state.networkView.search = event.target.value || "";
  renderNetwork();
}

async function applyNetworkFocus() {
  state.networkView.focus = $("#networkFocusInput")?.value?.trim() || "";
  state.networkView.focusType = $("#networkFocusType")?.value || "auto";
  state.networkView.community = "all";
  state.networkView.search = "";
  state.selectedNetworkNodeId = null;
  if ($("#networkSearchInput")) $("#networkSearchInput").value = "";
  setText("#networkProgressiveNote", state.networkView.focus ? "Tracing focused transaction network..." : "Loading full network...");
  await loadNetwork();
}

async function clearNetworkFocus() {
  state.networkView.focus = "";
  state.networkView.focusType = "auto";
  state.networkView.community = "all";
  state.networkView.search = "";
  state.selectedNetworkNodeId = null;
  if ($("#networkFocusInput")) $("#networkFocusInput").value = "";
  if ($("#networkFocusType")) $("#networkFocusType").value = "auto";
  if ($("#networkSearchInput")) $("#networkSearchInput").value = "";
  await loadNetwork();
}

function setNetworkMode(mode) {
  state.networkView.mode = ["money", "path", "investigation"].includes(mode) ? mode : "investigation";
  if (state.networkView.mode !== "path") {
    state.networkView.pathStart = null;
    state.networkView.pathEnd = null;
  }
  $$("[data-network-mode]").forEach((button) => button.classList.toggle("is-active", button.dataset.networkMode === state.networkView.mode));
  renderNetwork();
}

function selectNetworkNode(nodeId, graph) {
  if (state.networkView.mode === "path") {
    if (!state.networkView.pathStart || (state.networkView.pathStart && state.networkView.pathEnd)) {
      state.networkView.pathStart = nodeId;
      state.networkView.pathEnd = null;
    } else if (state.networkView.pathStart !== nodeId) {
      state.networkView.pathEnd = nodeId;
    }
  }
  state.selectedNetworkNodeId = nodeId;
  if (state.networkCy) {
    state.networkCy.nodes().forEach((node) => {
      const selected = node.id() === nodeId;
      node.toggleClass("selected-node", selected);
      node.data("displayLabel", selected ? node.data("label") : "");
    });
  }
  renderNetworkDetails(nodeId, graph);
  $("#networkDetail")?.classList.add("is-open");
  if (window.lucide) lucide.createIcons();
  if (state.networkView.mode === "path") renderNetwork();
}

function closeNetworkPanel() {
  state.selectedNetworkNodeId = null;
  $("#networkDetail")?.classList.remove("is-open");
  if (state.networkCy) {
    state.networkCy.nodes().forEach((node) => {
      node.removeClass("selected-node");
      node.data("displayLabel", "");
    });
  }
}

function highlightNeighborhood(nodeId) {
  if (!state.networkCy) return;
  const focus = state.networkCy.getElementById(nodeId);
  const neighborhood = focus.closedNeighborhood();
  state.networkCy.elements().addClass("is-neighborhood-dim");
  neighborhood.removeClass("is-neighborhood-dim").addClass("is-neighborhood-focus");
}

function clearNeighborhoodHighlight() {
  if (!state.networkCy) return;
  state.networkCy.elements().removeClass("is-neighborhood-dim is-neighborhood-focus");
}

function showNetworkHoverLabel(label, event) {
  const tooltip = $("#networkHoverLabel");
  if (!tooltip) return;
  tooltip.textContent = label;
  tooltip.classList.add("is-visible");
  const bounds = $("#networkCy")?.getBoundingClientRect() || { left: 0, top: 0 };
  tooltip.style.left = `${(event?.clientX || bounds.left) - bounds.left + 14}px`;
  tooltip.style.top = `${(event?.clientY || bounds.top) - bounds.top + 14}px`;
}

function hideNetworkHoverLabel() {
  $("#networkHoverLabel")?.classList.remove("is-visible");
}

function calculateWeightedDegrees(nodes, links) {
  const degrees = new Map(nodes.map((node) => [node.id, 0]));
  links.forEach((link) => {
    const weight = Math.max(1, Number(link.weight || 1));
    degrees.set(link.source, (degrees.get(link.source) || 0) + weight);
    degrees.set(link.target, (degrees.get(link.target) || 0) + weight);
  });
  return degrees;
}

function detectCommunitiesLouvain(nodes, links) {
  const community = new Map(nodes.map((node, index) => [node.id, index]));
  const adjacency = weightedAdjacency(nodes, links, false);
  for (let iteration = 0; iteration < 12; iteration += 1) {
    let moved = false;
    nodes.forEach((node) => {
      const neighborWeights = new Map();
      (adjacency.get(node.id) || []).forEach(({ target, weight }) => {
        const targetCommunity = community.get(target);
        neighborWeights.set(targetCommunity, (neighborWeights.get(targetCommunity) || 0) + weight);
      });
      const best = Array.from(neighborWeights.entries()).sort((a, b) => b[1] - a[1])[0];
      if (best && best[0] !== community.get(node.id)) {
        community.set(node.id, best[0]);
        moved = true;
      }
    });
    if (!moved) break;
  }
  const normalized = new Map();
  let next = 1;
  nodes.forEach((node) => {
    const raw = community.get(node.id);
    if (!normalized.has(raw)) normalized.set(raw, next++);
    community.set(node.id, normalized.get(raw));
  });
  return community;
}

function calculatePageRank(nodes, links) {
  const ids = nodes.map((node) => node.id);
  const rank = new Map(ids.map((id) => [id, 1 / Math.max(1, ids.length)]));
  const outgoing = weightedAdjacency(nodes, links, true);
  const damping = 0.85;
  for (let iteration = 0; iteration < 28; iteration += 1) {
    const next = new Map(ids.map((id) => [id, (1 - damping) / Math.max(1, ids.length)]));
    ids.forEach((id) => {
      const edges = outgoing.get(id) || [];
      const total = edges.reduce((sum, edge) => sum + edge.weight, 0) || 1;
      edges.forEach((edge) => {
        next.set(edge.target, (next.get(edge.target) || 0) + damping * (rank.get(id) || 0) * (edge.weight / total));
      });
    });
    ids.forEach((id) => rank.set(id, next.get(id) || 0));
  }
  return rank;
}

function calculateBetweennessCentrality(nodes, links) {
  const ids = nodes.map((node) => node.id);
  const adjacency = weightedAdjacency(nodes, links, false);
  const sample = ids.length > 450 ? ids.filter((_, index) => index % Math.ceil(ids.length / 90) === 0).slice(0, 90) : ids;
  const centrality = new Map(ids.map((id) => [id, 0]));
  sample.forEach((source) => {
    const stack = [];
    const predecessors = new Map(ids.map((id) => [id, []]));
    const sigma = new Map(ids.map((id) => [id, 0]));
    const distance = new Map(ids.map((id) => [id, -1]));
    sigma.set(source, 1);
    distance.set(source, 0);
    const queue = [source];
    while (queue.length) {
      const vertex = queue.shift();
      stack.push(vertex);
      (adjacency.get(vertex) || []).forEach(({ target }) => {
        if (distance.get(target) < 0) {
          queue.push(target);
          distance.set(target, distance.get(vertex) + 1);
        }
        if (distance.get(target) === distance.get(vertex) + 1) {
          sigma.set(target, sigma.get(target) + sigma.get(vertex));
          predecessors.get(target).push(vertex);
        }
      });
    }
    const delta = new Map(ids.map((id) => [id, 0]));
    while (stack.length) {
      const w = stack.pop();
      predecessors.get(w).forEach((v) => {
        const value = (sigma.get(v) / Math.max(1, sigma.get(w))) * (1 + delta.get(w));
        delta.set(v, delta.get(v) + value);
      });
      if (w !== source) centrality.set(w, centrality.get(w) + delta.get(w));
    }
  });
  const max = Math.max(1, ...Array.from(centrality.values()));
  centrality.forEach((value, key) => centrality.set(key, value / max));
  return centrality;
}

function weightedAdjacency(nodes, links, directed) {
  const adjacency = new Map(nodes.map((node) => [node.id, []]));
  links.forEach((link) => {
    const weight = Math.max(1, Number(link.weight || 1));
    if (adjacency.has(link.source)) adjacency.get(link.source).push({ target: link.target, weight, link });
    if (!directed && adjacency.has(link.target)) adjacency.get(link.target).push({ target: link.source, weight, link });
  });
  return adjacency;
}

function estimateNodeRisk(node, centrality, pageRank, betweenness) {
  const explicit = Number(node.risk_score || node.metadata?.risk_score || node.metadata?.risk || 0);
  if (explicit) return Math.max(1, Math.min(100, explicit));
  const typeBase = {
    suspect: 48,
    financial_account: 42,
    case: 30,
    bank_manager: 34,
    bank: 26,
    ifsc: 24,
    branch: 24,
    dead_end: 52,
  }[node.type] || 22;
  return Math.max(1, Math.min(100, typeBase + centrality * 32 + pageRank * 900 + betweenness * 18 + Math.log1p(node.case_count || 0) * 5));
}

function riskColor(risk) {
  if (risk >= 78) return "#ff5d5d";
  if (risk >= 58) return "#f7b955";
  if (risk >= 36) return "#4ea8ff";
  return "#00d4aa";
}

function communityColor(community) {
  const palette = ["#00d4aa", "#4ea8ff", "#f7b955", "#c084fc", "#fb7185", "#60a5fa", "#34d399", "#f97316", "#a78bfa", "#22d3ee"];
  return palette[Math.abs(Number(community || 0)) % palette.length];
}

function summarizeCommunities(nodes, links) {
  const groups = new Map();
  nodes.forEach((node) => {
    const id = node._community ?? 0;
    if (!groups.has(id)) groups.set(id, { id, nodeCount: 0, linkCount: 0, risk: 0, topNode: node });
    const group = groups.get(id);
    group.nodeCount += 1;
    group.risk += node._risk;
    if (node._importance > group.topNode._importance) group.topNode = node;
  });
  links.forEach((link) => {
    const source = nodes.find((node) => node.id === link.source);
    const target = nodes.find((node) => node.id === link.target);
    if (source && target && source._community === target._community) {
      groups.get(source._community).linkCount += 1;
    }
  });
  return Array.from(groups.values())
    .map((group) => ({ ...group, avgRisk: group.risk / Math.max(1, group.nodeCount) }))
    .sort((a, b) => b.nodeCount - a.nodeCount);
}

function graphDensity(nodeCount, linkCount) {
  if (nodeCount < 2) return "0.00";
  return (linkCount / (nodeCount * (nodeCount - 1))).toFixed(3);
}

function isMoneyRelationship(relationship) {
  return ["TRANSFERRED_TO", "HAS_FINANCIAL_SOURCE", "HAS_FINANCIAL_TARGET", "ACCOUNT_HELD_AT_BANK", "ROUTED_BY_IFSC", "SERVICED_BY_BRANCH", "BRANCH_MANAGER_CONTACT", "TRAIL_ENDS_AT"].includes(relationship);
}

function networkLinkDate(link, nodeMap) {
  const transactionDate = (link.metadata?.transactions || [])
    .map((item) => new Date(item.occurred_at || item.date || ""))
    .filter((date) => !Number.isNaN(date.getTime()))
    .sort((a, b) => a - b)[0];
  if (transactionDate) return transactionDate;
  const sourceDate = new Date(nodeMap.get(link.source)?.metadata?.incident_at || "");
  if (!Number.isNaN(sourceDate.getTime())) return sourceDate;
  const targetDate = new Date(nodeMap.get(link.target)?.metadata?.incident_at || "");
  return Number.isNaN(targetDate.getTime()) ? null : targetDate;
}

function networkTimeCutoff(base) {
  const dates = base.links.map((link) => link._date).filter(Boolean).sort((a, b) => a - b);
  if (!dates.length || state.networkView.timePercent >= 100) return null;
  const index = Math.max(0, Math.min(dates.length - 1, Math.round((state.networkView.timePercent / 100) * (dates.length - 1))));
  return dates[index];
}

function updateNetworkTimeLabel(base) {
  const label = $("#networkTimeLabel");
  if (!label) return;
  const cutoff = networkTimeCutoff(base);
  label.textContent = cutoff ? `Through ${cutoff.toLocaleDateString()}` : "All time";
}

function detectCircularMoneyFlows(links) {
  const transferLinks = links.filter((link) => link.relationship === "TRANSFERRED_TO");
  const adjacency = new Map();
  transferLinks.forEach((link) => {
    if (!adjacency.has(link.source)) adjacency.set(link.source, []);
    adjacency.get(link.source).push(link);
  });
  const circular = new Set();
  transferLinks.forEach((start) => {
    const stack = [{ node: start.target, path: [start], seen: new Set([start.source, start.target]) }];
    while (stack.length) {
      const current = stack.pop();
      if (current.path.length > 6) continue;
      for (const link of adjacency.get(current.node) || []) {
        if (link.target === start.source) {
          [...current.path, link].forEach((item) => circular.add(edgeKey(item)));
        } else if (!current.seen.has(link.target)) {
          const nextSeen = new Set(current.seen);
          nextSeen.add(link.target);
          stack.push({ node: link.target, path: [...current.path, link], seen: nextSeen });
        }
      }
    }
  });
  return circular;
}

function detectSuspiciousAccountChains(nodes, links) {
  const nodeMap = new Map(nodes.map((node) => [node.id, node]));
  const transferLinks = links.filter((link) => link.relationship === "TRANSFERRED_TO");
  const incoming = new Set(transferLinks.map((link) => link.target));
  const starts = transferLinks.filter((link) => !incoming.has(link.source)).slice(0, 30);
  const adjacency = new Map();
  transferLinks.forEach((link) => {
    if (!adjacency.has(link.source)) adjacency.set(link.source, []);
    adjacency.get(link.source).push(link);
  });
  const chains = [];
  starts.forEach((start) => {
    const path = [start];
    let current = start.target;
    const seen = new Set([start.source, start.target]);
    while ((adjacency.get(current) || []).length && path.length < 7) {
      const next = (adjacency.get(current) || [])[0];
      path.push(next);
      if (seen.has(next.target)) break;
      seen.add(next.target);
      current = next.target;
    }
    if (path.length >= 2) {
      const labels = [path[0].source, ...path.map((link) => link.target)].map((id) => nodeMap.get(id)?.label || id);
      chains.push({ links: path, labels });
    }
  });
  return chains;
}

function shortestNetworkPath(start, end, links) {
  const adjacency = new Map();
  links.forEach((link) => {
    if (!adjacency.has(link.source)) adjacency.set(link.source, []);
    if (!adjacency.has(link.target)) adjacency.set(link.target, []);
    adjacency.get(link.source).push({ next: link.target, link });
    adjacency.get(link.target).push({ next: link.source, link });
  });
  const queue = [start];
  const previous = new Map([[start, null]]);
  while (queue.length) {
    const current = queue.shift();
    if (current === end) break;
    for (const edge of adjacency.get(current) || []) {
      if (!previous.has(edge.next)) {
        previous.set(edge.next, { node: current, link: edge.link });
        queue.push(edge.next);
      }
    }
  }
  if (!previous.has(end)) return [];
  const path = [];
  let cursor = end;
  while (previous.get(cursor)) {
    const item = previous.get(cursor);
    path.unshift(item.link);
    cursor = item.node;
  }
  return path;
}

function edgeKey(link) {
  return `${link.source}->${link.target}:${link.relationship}`;
}

function relationshipLabel(value) {
  return String(value || "").replace(/_/g, " ").toLowerCase();
}

function nodeLabel(nodeId, prepared) {
  return prepared.nodeMap?.get(nodeId)?.label || nodeId;
}

function progressiveNetworkNote(prepared) {
  const engine = window.cytoscape ? "Cytoscape.js" : "Canvas fallback";
  const disclosure = prepared.metrics.totalNodes > prepared.filteredNodeCount
    ? `Showing ${formatCount(prepared.filteredNodeCount)} of ${formatCount(prepared.metrics.totalNodes)} nodes`
    : `${formatCount(prepared.filteredNodeCount)} nodes visible`;
  const path = state.networkView.mode === "path"
    ? state.networkView.pathStart && state.networkView.pathEnd
      ? "Shortest path highlighted"
      : state.networkView.pathStart
        ? "Select a second node to compute shortest path"
        : "Select a start node"
    : "Labels appear on hover";
  return `${engine} / ${disclosure} / ${path}`;
}

function exportNetwork(kind) {
  const prepared = state.networkPrepared;
  if (!prepared?.nodes?.length) return;
  if (kind === "png") {
    const dataUrl = state.networkCy
      ? state.networkCy.png({ full: true, scale: 2, bg: "#0a0f1f" })
      : $("#networkCanvasFallback")?.toDataURL("image/png");
    if (dataUrl) downloadDataUrl(dataUrl, "ksp-criminal-network.png");
  } else if (kind === "graphml") {
    downloadText("ksp-criminal-network.graphml", buildGraphMl(prepared), "application/graphml+xml");
  } else if (kind === "csv") {
    downloadText("ksp-criminal-network-nodes.csv", networkNodesCsv(prepared), "text/csv");
    setTimeout(() => downloadText("ksp-criminal-network-edges.csv", networkEdgesCsv(prepared), "text/csv"), 250);
  } else if (kind === "pdf") {
    exportNetworkPdf(prepared);
  }
}

function downloadDataUrl(dataUrl, filename) {
  const link = document.createElement("a");
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
}

function downloadText(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  downloadDataUrl(url, filename);
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function networkNodesCsv(prepared) {
  const rows = [["id", "label", "type", "community", "risk_score", "degree", "pagerank", "betweenness", "case_count"]];
  prepared.nodes.forEach((node) => rows.push([node.id, node.label, node.type, node._community, Math.round(node._risk), node._degree, node._pagerank.toFixed(6), node._betweenness.toFixed(6), node.case_count || 0]));
  return rows.map(csvRow).join("\n");
}

function networkEdgesCsv(prepared) {
  const rows = [["source", "target", "relationship", "weight", "money_flow", "circular_flow", "case_ids"]];
  prepared.links.forEach((link) => rows.push([link.source, link.target, link.relationship, link.weight || 1, link._money ? "yes" : "no", link._circular ? "yes" : "no", (link.case_ids || []).join("|")]));
  return rows.map(csvRow).join("\n");
}

function csvRow(values) {
  return values.map((value) => `"${String(value ?? "").replace(/"/g, '""')}"`).join(",");
}

function buildGraphMl(prepared) {
  const nodes = prepared.nodes.map((node) => `
    <node id="${escapeXml(node.id)}">
      <data key="label">${escapeXml(node.label)}</data>
      <data key="type">${escapeXml(node.type)}</data>
      <data key="community">${escapeXml(node._community)}</data>
      <data key="risk_score">${escapeXml(Math.round(node._risk))}</data>
      <data key="pagerank">${escapeXml(node._pagerank.toFixed(6))}</data>
      <data key="betweenness">${escapeXml(node._betweenness.toFixed(6))}</data>
    </node>`).join("");
  const edges = prepared.links.map((link, index) => `
    <edge id="e${index}" source="${escapeXml(link.source)}" target="${escapeXml(link.target)}">
      <data key="relationship">${escapeXml(link.relationship)}</data>
      <data key="weight">${escapeXml(link.weight || 1)}</data>
      <data key="circular">${escapeXml(link._circular ? "true" : "false")}</data>
    </edge>`).join("");
  return `<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="label" for="node" attr.name="label" attr.type="string"/>
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="community" for="node" attr.name="community" attr.type="string"/>
  <key id="risk_score" for="node" attr.name="risk_score" attr.type="double"/>
  <key id="pagerank" for="node" attr.name="pagerank" attr.type="double"/>
  <key id="betweenness" for="node" attr.name="betweenness" attr.type="double"/>
  <key id="relationship" for="edge" attr.name="relationship" attr.type="string"/>
  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>
  <key id="circular" for="edge" attr.name="circular" attr.type="boolean"/>
  <graph id="KSPCriminalNetwork" edgedefault="directed">${nodes}${edges}
  </graph>
</graphml>`;
}

function escapeXml(value) {
  return String(value ?? "").replace(/[<>&'"]/g, (char) => ({
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    "'": "&apos;",
    '"': "&quot;",
  }[char]));
}

function exportNetworkPdf(prepared) {
  const image = state.networkCy
    ? state.networkCy.png({ full: true, scale: 1.5, bg: "#0a0f1f" })
    : $("#networkCanvasFallback")?.toDataURL("image/png");
  const popup = window.open("", "_blank", "noopener,noreferrer,width=1200,height=900");
  if (!popup) return;
  popup.document.write(`
    <html>
      <head><title>KSP Criminal Network Analysis</title></head>
      <body style="margin:0;background:#0a0f1f;color:#f8fafc;font-family:Inter,Arial,sans-serif;">
        <section style="padding:24px;">
          <h1 style="margin:0 0 6px;">KSP Criminal Network Analysis</h1>
          <p style="margin:0 0 18px;color:#94a3b8;">Nodes ${prepared.filteredNodeCount} / Connections ${prepared.filteredLinkCount} / Cells ${prepared.metrics.communities}</p>
          ${image ? `<img src="${image}" style="width:100%;border:1px solid rgba(255,255,255,.12);border-radius:12px;" />` : ""}
          <p style="color:#94a3b8;">Use the browser print dialog to save this intelligence view as PDF.</p>
        </section>
        <script>setTimeout(() => window.print(), 400);<\/script>
      </body>
    </html>
  `);
  popup.document.close();
}

function stableHash(value) {
  return String(value || "").split("").reduce((hash, char) => ((hash << 5) - hash + char.charCodeAt(0)) | 0, 0);
}

function profilePhotoForName(name) {
  const clean = String(name || "").trim();
  if (!clean || clean.toLowerCase() === "unknown") return "";
  return PROFILE_PHOTOS[Math.abs(stableHash(clean)) % PROFILE_PHOTOS.length];
}

function networkNodePhoto(node) {
  if (node?.type !== "suspect") return "";
  const metadata = node.metadata || {};
  return profilePhotoForName(metadata.suspect_name || metadata.account_holder || node.label);
}

function networkNodeDisplayLabel(node) {
  const metadata = node.metadata || {};
  if (node.type === "financial_account") {
    return metadata.account_holder ? `${metadata.account_holder} / ${metadata.account || node.label}` : node.label;
  }
  if (node.type === "case") return metadata.fir_number || node.label;
  return node.label;
}

function networkNodeSearchText(node) {
  const metadata = node.metadata || {};
  return [
    node.id,
    node.label,
    node.type,
    ...(node.districts || []),
    metadata.account,
    metadata.account_holder,
    metadata.suspect_name,
    metadata.victim_name,
    metadata.complainant_name,
    metadata.bank_name,
    metadata.ifsc_code,
    metadata.branch,
    metadata.bank_manager_phone,
    ...(metadata.accounts || []),
    ...(metadata.linked_cases || []).map((item) => `${item?.fir_number || ""} ${item?.case_number || ""}`),
  ].filter(Boolean).join(" ").toLowerCase();
}

function renderEntityIdentityCard(node, graph) {
  const metadata = node.metadata || {};
  const owner = metadata.suspect_name || metadata.account_holder || personOwnerForNode(node, graph);
  const photo = profilePhotoForName(owner);
  const typeLabel = labelValue(node.type);
  const subtitle = node.type === "financial_account"
    ? `${metadata.account || node.label} / ${metadata.bank_name || "Bank not recorded"}`
    : node.type === "case"
      ? `${metadata.fir_number || node.label} / ${labelValue(metadata.status || "case")}`
      : owner || typeLabel;
  return `
    <article class="node-profile-card">
      <div class="node-profile-photo ${photo ? "" : "is-empty"}">
        ${photo ? `<img src="${escapeHtml(photo)}" alt="${escapeHtml(owner || node.label)} record photo" loading="lazy" />` : `<i data-lucide="${node.type === "financial_account" ? "landmark" : "user-round"}"></i>`}
      </div>
      <div>
        <span>${escapeHtml(typeLabel)}</span>
        <strong>${escapeHtml(networkNodeDisplayLabel(node))}</strong>
        <p>${escapeHtml(subtitle || "Evidence-linked network entity")}</p>
      </div>
    </article>
    <div class="detail-section node-identity-card">
      <h4>Who this node belongs to</h4>
      <div class="detail-grid">
        ${detailRow("Person / holder", owner)}
        ${detailRow("Account number", metadata.account || (node.type === "financial_account" ? node.label : ""))}
        ${detailRow("Bank name", metadata.bank_name)}
        ${detailRow("IFSC code", metadata.ifsc_code)}
        ${detailRow("Branch", metadata.branch)}
        ${detailRow("Bank manager number", metadata.bank_manager_phone)}
        ${detailRow("Linked accounts", (metadata.accounts || []).join(", "))}
        ${detailRow("Linked FIRs", linkedFirLabels(node, graph).join(", "))}
      </div>
    </div>
  `;
}

function linkedFirLabels(node, graph) {
  const metadata = node.metadata || {};
  const fromMetadata = [
    ...(metadata.cases || []),
    ...(metadata.linked_cases || []),
  ].map((item) => item?.fir_number).filter(Boolean);
  const fromTransfers = transactionsForNode(node, graph)
    .map((tx) => tx.case_id ? caseLabelById(tx.case_id, graph) : "")
    .filter(Boolean);
  return [...new Set([...fromMetadata, ...fromTransfers])];
}

function personOwnerForNode(node, graph) {
  const metadata = node.metadata || {};
  if (metadata.account_holder || metadata.suspect_name) return metadata.account_holder || metadata.suspect_name;
  const transfers = transactionsForNode(node, graph);
  for (const tx of transfers) {
    if (metadata.account && tx.source_account === metadata.account) return tx.source_account_holder;
    if (metadata.account && tx.target_account === metadata.account) return tx.target_account_holder;
    if (tx.source_account_holder) return tx.source_account_holder;
    if (tx.target_account_holder) return tx.target_account_holder;
  }
  return "";
}

function transactionsForNode(node, graph) {
  const metadata = node?.metadata || {};
  const direct = [
    ...(metadata.incoming_transfers || []),
    ...(metadata.outgoing_transfers || []),
    ...(metadata.financial_trails || []),
    ...(metadata.transactions || []),
    ...(metadata.transfers || []),
  ];
  (graph?.links || []).forEach((link) => {
    if (link.source === node.id || link.target === node.id) {
      direct.push(...(link.metadata?.transactions || []));
    }
  });
  return uniqueBy(direct, (tx) => tx.transaction_id || `${tx.source_account}-${tx.target_account}-${tx.amount}-${tx.occurred_at}`);
}

function renderNetworkDetails(nodeId, graph) {
  const panel = $("#networkDetail");
  const node = (graph?.nodes || []).find((item) => item.id === nodeId);
  const closeButton = `<button class="icon-button network-panel-close" type="button" id="networkPanelClose" title="Close node panel" aria-label="Close node panel"><i data-lucide="x"></i></button>`;
  if (!node) {
    panel.innerHTML = `
      ${closeButton}
      <p class="eyebrow">Node details</p>
      <h3>Select a graph node</h3>
      <p class="muted-copy">Click Ravi Kumar, a FIR node, or an account node to inspect the evidence-bound trail.</p>
    `;
    $("#networkPanelClose")?.addEventListener("click", closeNetworkPanel);
    return;
  }
  const title = node.type === "case" ? `FIR ${node.label}` : node.label;
  const body =
    node.type === "suspect" ? renderSuspectNetworkDetail(node, graph) :
    node.type === "case" ? renderCaseNetworkDetail(node, graph) :
    node.type === "financial_account" ? renderAccountNetworkDetail(node, graph) :
    renderMetadataNetworkDetail(node, graph);
  panel.innerHTML = `
    ${closeButton}
    <p class="eyebrow">${escapeHtml(labelValue(node.type))}</p>
    <h3>${escapeHtml(title)}</h3>
    ${renderEntityIdentityCard(node, graph)}
    ${body}
  `;
  $("#networkPanelClose")?.addEventListener("click", closeNetworkPanel);
}

function renderSuspectNetworkDetail(node, graph) {
  const metadata = node.metadata || {};
  const cases = uniqueBy([...(metadata.cases || []), ...(metadata.linked_cases || [])], (item) => item.case_id || item.fir_number);
  const trails = cases.flatMap((caseItem) => buildMoneyTrailsForCase(caseItem.case_id, graph));
  const accountTrails = buildMoneyTrailsForNode(node, graph);
  const trailHtml = trails.length || accountTrails.length
    ? renderMoneyTrails([...trails, ...accountTrails], graph)
    : renderTransferCards(metadata.financial_trails || transactionsForNode(node, graph), graph);
  const connectionSignal = trails.length >= 2
    ? `${trails.length} reachable money path(s) are linked through accessible case transactions.`
    : "";
  return `
    <div class="detail-grid">
      ${detailRow("Suspect name", metadata.suspect_name || node.label)}
      ${detailRow("Account holder", metadata.account_holder)}
      ${detailRow("Accounts", (metadata.accounts || []).join(", "))}
      ${detailRow("Named in accessible cases", cases.length || node.case_count || 0)}
      ${detailRow("Districts", (node.districts || []).join(", "))}
      ${detailRow("Connection signal", connectionSignal)}
    </div>
    <div class="detail-section">
      <h4>Cases</h4>
      ${cases.length ? cases.map((caseItem) => caseNetworkCard(caseItem)).join("") : `<p class="muted-copy">No accessible cases are attached to this suspect.</p>`}
    </div>
    <div class="detail-section">
      <h4>Chain-linked transfers</h4>
      ${trailHtml}
    </div>
  `;
}

function renderCaseNetworkDetail(node, graph) {
  const metadata = node.metadata || {};
  const trails = buildMoneyTrailsForCase(metadata.case_id, graph);
  return `
    <div class="detail-grid">
      ${detailRow("FIR number", metadata.fir_number || node.label)}
      ${detailRow("Case no", metadata.case_number || metadata.case_id)}
      ${detailRow("Status", labelValue(metadata.status))}
      ${detailRow("District", metadata.district)}
      ${detailRow("Suspect", metadata.suspect_name)}
      ${detailRow("Victim", metadata.victim_name)}
      ${detailRow("Crime type", metadata.case_type)}
      ${detailRow("Modus operandi", metadata.modus_operandi)}
      ${detailRow("Summary", metadata.summary)}
    </div>
    <div class="detail-section">
      <h4>Chain-linked transfers for this FIR</h4>
      ${renderMoneyTrails(trails, graph)}
    </div>
  `;
}

function renderAccountNetworkDetail(node, graph) {
  const metadata = node.metadata || {};
  const incoming = metadata.incoming_transfers || [];
  const outgoing = metadata.outgoing_transfers || [];
  const cases = metadata.linked_cases || [];
  const splitNote = outgoing.length >= 2 ? `${outgoing.length} outgoing transfers indicate amount splitting from this account.` : "";
  return `
    <div class="detail-grid">
      ${detailRow("Account", metadata.account || node.label)}
      ${detailRow("Account holder", metadata.account_holder)}
      ${detailRow("Bank", metadata.bank_name)}
      ${detailRow("IFSC", metadata.ifsc_code)}
      ${detailRow("Branch", metadata.branch)}
      ${detailRow("Manager contact", metadata.bank_manager_phone)}
      ${detailRow("Districts", (node.districts || []).join(", "))}
      ${detailRow("Linked cases", cases.map((item) => item.fir_number).join(", ") || "None")}
      ${detailRow("Split signal", splitNote)}
    </div>
    <div class="detail-section">
      <h4>Incoming</h4>
      ${renderTransferCards(incoming, graph)}
    </div>
    <div class="detail-section">
      <h4>Outgoing</h4>
      ${renderTransferCards(outgoing, graph)}
    </div>
    <div class="detail-section">
      <h4>Chain-linked transfers from this account</h4>
      ${renderMoneyTrails(buildMoneyTrailsForNode(node, graph), graph)}
    </div>
    <p class="muted-copy">Owner, bank, IFSC, branch and manager fields are shown when they are present in imported bank transaction records.</p>
  `;
}

function renderMetadataNetworkDetail(node, graph) {
  const metadata = node.metadata || {};
  const transfers = metadata.transactions || [];
  if (node.type === "dead_end") {
    return `
      <div class="detail-grid">
        ${detailRow("Final account", metadata.account)}
        ${detailRow("Account holder", personOwnerForNode(node, graph))}
        ${detailRow("Reason", metadata.reason)}
        ${detailRow("Districts", (node.districts || []).join(", "))}
      </div>
      <p class="muted-copy">This is a dead-end only in the accessible records. More bank data may reveal later transfers.</p>
    `;
  }
  return `
    <div class="detail-grid">
      ${detailRow("Bank", metadata.bank_name)}
      ${detailRow("IFSC", metadata.ifsc_code)}
      ${detailRow("Branch", metadata.branch)}
      ${detailRow("Manager contact", metadata.bank_manager_phone)}
      ${detailRow("Accounts", (metadata.accounts || []).join(", "))}
      ${detailRow("Districts", (node.districts || []).join(", "))}
    </div>
    <div class="detail-section">
      <h4>Linked transfers</h4>
      ${renderTransferCards(transfers, graph)}
    </div>
    <div class="detail-section">
      <h4>Chain-linked transfers through this node</h4>
      ${renderMoneyTrails(buildMoneyTrailsForNode(node, graph), graph)}
    </div>
  `;
}

function caseNetworkCard(caseItem) {
  return `
    <article class="trail-card">
      <div class="trail-path">
        <b>${escapeHtml(caseItem.fir_number)}</b>
        <span>${escapeHtml(labelValue(caseItem.status))}</span>
      </div>
      <p>Case no: ${escapeHtml(caseItem.case_number || caseItem.case_id)} / District: ${escapeHtml(caseItem.district || "Unknown")}</p>
      <p>${escapeHtml(caseItem.summary || "No summary recorded.")}</p>
    </article>
  `;
}

function buildMoneyTrailsForCase(caseId, graph) {
  if (!caseId) return [];
  const links = graph.links || [];
  const sourceAccounts = links
    .filter((link) => link.relationship === "HAS_FINANCIAL_SOURCE" && link.source === `case:${caseId}`)
    .map((link) => link.target);
  const transferLinks = links.filter((link) => link.relationship === "TRANSFERRED_TO");
  const adjacency = new Map();
  transferLinks.forEach((link) => {
    if (!adjacency.has(link.source)) adjacency.set(link.source, []);
    adjacency.get(link.source).push(link);
  });
  const trails = [];
  [...new Set(sourceAccounts)].forEach((sourceAccount) => {
    walkMoneyTrail(sourceAccount, [], new Set([sourceAccount]), adjacency, trails);
  });
  return trails;
}

function buildMoneyTrailsForNode(node, graph) {
  if (!node || !graph) return [];
  if (node.type === "case") return buildMoneyTrailsForCase(node.metadata?.case_id, graph);
  const sources = sourceAccountNodeIdsForNode(node, graph);
  return buildMoneyTrailsFromSources(sources, graph);
}

function buildMoneyTrailsFromSources(sourceIds, graph) {
  const transferLinks = (graph.links || []).filter((link) => link.relationship === "TRANSFERRED_TO");
  const adjacency = new Map();
  transferLinks.forEach((link) => {
    if (!adjacency.has(link.source)) adjacency.set(link.source, []);
    adjacency.get(link.source).push(link);
  });
  const trails = [];
  [...new Set(sourceIds)].forEach((sourceAccount) => {
    walkMoneyTrail(sourceAccount, [], new Set([sourceAccount]), adjacency, trails);
  });
  return trails;
}

function sourceAccountNodeIdsForNode(node, graph) {
  const metadata = node.metadata || {};
  if (node.type === "financial_account") return [node.id];
  const ids = new Set();
  const accountLabels = new Set((metadata.accounts || []).map((account) => String(account)));
  if (metadata.account) accountLabels.add(String(metadata.account));
  (graph.nodes || []).forEach((candidate) => {
    if (candidate.type === "financial_account" && accountLabels.has(String(candidate.metadata?.account || candidate.label))) {
      ids.add(candidate.id);
    }
  });
  (graph.links || []).forEach((link) => {
    if (link.relationship === "ACCOUNT_HOLDER_OF" && link.source === node.id) ids.add(link.target);
    if (["ACCOUNT_HELD_AT_BANK", "ROUTED_BY_IFSC", "SERVICED_BY_BRANCH", "BRANCH_MANAGER_CONTACT"].includes(link.relationship)) {
      if (link.source === node.id && String(link.target).startsWith("account:")) ids.add(link.target);
      if (link.target === node.id && String(link.source).startsWith("account:")) ids.add(link.source);
    }
    if (node.type === "case" && link.relationship === "HAS_FINANCIAL_SOURCE" && link.source === node.id) ids.add(link.target);
  });
  transactionsForNode(node, graph).forEach((tx) => {
    const source = findAccountNodeByLabel(tx.source_account, graph);
    const target = findAccountNodeByLabel(tx.target_account, graph);
    if (source) ids.add(source.id);
    if (target && node.type !== "case") ids.add(target.id);
  });
  return [...ids];
}

function findAccountNodeByLabel(account, graph) {
  if (!account) return null;
  return (graph.nodes || []).find((node) => node.type === "financial_account" && (node.metadata?.account === account || node.label === account));
}

function walkMoneyTrail(currentNodeId, path, visited, adjacency, trails) {
  const outgoing = adjacency.get(currentNodeId) || [];
  if (!outgoing.length) {
    if (path.length) trails.push(path);
    return;
  }
  outgoing.slice(0, 12).forEach((link) => {
    const nextPath = [...path, link];
    if (visited.has(link.target)) {
      trails.push(nextPath);
      return;
    }
    const nextVisited = new Set(visited);
    nextVisited.add(link.target);
    walkMoneyTrail(link.target, nextPath, nextVisited, adjacency, trails);
  });
}

function renderMoneyTrails(trails, graph) {
  if (!trails.length) {
    return `<p class="muted-copy">No financial transfers are linked to the accessible case records for this node.</p>`;
  }
  const nodes = new Map((graph.nodes || []).map((node) => [node.id, node]));
  return trails
    .slice(0, 12)
    .map((trail) => {
      const pathIds = [trail[0].source, ...trail.map((link) => link.target)];
      const transactions = trail.flatMap((link) => link.metadata?.transactions || []);
      const lastNode = nodes.get(pathIds[pathIds.length - 1]);
      const lastParty = personOwnerForNode(lastNode || { metadata: {} }, graph) || lastNode?.metadata?.account || lastNode?.label || pathIds[pathIds.length - 1];
      return `
        <article class="trail-card">
          <div class="trail-path">
            ${pathIds.map((id) => renderChainNode(nodes.get(id), id)).join("<span>&rarr;</span>")}
          </div>
          ${transactions.map((transaction) => transferFact(transaction)).join("")}
          <p>Last recorded party/account: ${escapeHtml(lastParty)}. Continue bank-data import to extend beyond any dead-end node.</p>
        </article>
      `;
    })
    .join("");
}

function renderTransferCards(transfers, graph) {
  if (!transfers.length) return `<p class="muted-copy">No transfers recorded for this direction.</p>`;
  return transfers.slice(0, 12).map((transfer) => `
    <article class="trail-card">
      <div class="transfer-party-grid">
        ${renderTransferParty("From", transfer, "source")}
        ${renderTransferParty("To", transfer, "target")}
      </div>
      ${transferFact(transfer)}
      ${transfer.case_id ? `<p>Linked case: ${escapeHtml(caseLabelById(transfer.case_id, graph))}</p>` : ""}
    </article>
  `).join("");
}

function renderChainNode(node, fallbackId) {
  const metadata = node?.metadata || {};
  const owner = metadata.account_holder || metadata.suspect_name || "";
  const account = metadata.account || node?.label || fallbackId;
  const bank = [metadata.bank_name, metadata.ifsc_code].filter(Boolean).join(" / ");
  return `
    <b class="chain-node-card">
      <span>${escapeHtml(owner || labelValue(node?.type || "account"))}</span>
      <strong>${escapeHtml(account)}</strong>
      ${bank ? `<small>${escapeHtml(bank)}</small>` : ""}
    </b>
  `;
}

function renderTransferParty(label, transfer, side) {
  const holder = transfer[`${side}_account_holder`] || "Holder not recorded";
  const account = transfer[`${side}_account`] || "Account not recorded";
  const bank = transfer[`${side}_bank_name`] || "Bank not recorded";
  const ifsc = transfer[`${side}_ifsc_code`] || "IFSC not recorded";
  const branch = transfer[`${side}_branch`] || "Branch not recorded";
  const manager = transfer[`${side}_bank_manager_phone`] || "Manager phone not recorded";
  const photo = profilePhotoForName(holder);
  return `
    <div class="transfer-party">
      <div class="mini-person-photo ${photo ? "" : "is-empty"}">
        ${photo ? `<img src="${escapeHtml(photo)}" alt="${escapeHtml(holder)} record photo" loading="lazy" />` : `<i data-lucide="user-round"></i>`}
      </div>
      <div>
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(holder)}</strong>
        <p>${escapeHtml(account)}</p>
        <small>${escapeHtml(bank)} / ${escapeHtml(ifsc)} / ${escapeHtml(branch)}</small>
        <small>Manager: ${escapeHtml(manager)}</small>
      </div>
    </div>
  `;
}

function transferFact(transaction) {
  return `<p class="transfer-fact">${escapeHtml(formatNetworkAmount(transaction.amount, transaction.currency))} / ${escapeHtml(formatDateSafe(transaction.occurred_at))} / ${escapeHtml(transaction.description || "No description recorded.")}</p>`;
}

function caseLabelById(caseId, graph) {
  const node = (graph.nodes || []).find((item) => item.id === `case:${caseId}`);
  return node?.metadata?.fir_number || caseId;
}

function detailRow(label, value) {
  if (value === null || value === undefined || value === "") return "";
  return `
    <div class="detail-row">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `;
}

function uniqueBy(items, keyFn) {
  const seen = new Set();
  return items.filter((item) => {
    const key = keyFn(item);
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function formatNetworkAmount(value, currency = "INR") {
  return Number(value || 0).toLocaleString("en-IN", {
    style: "currency",
    currency: currency || "INR",
    maximumFractionDigits: 0,
  });
}

function formatDateSafe(value) {
  if (!value) return "No date recorded";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString(state.language === "kn" ? "kn-IN" : undefined);
}

function renderFinancial() {
  const data = state.financial;
  if (!data) return;
  $("#financialSummary").innerHTML = [
    metric(t("transactions"), data.transaction_count, t("visibleFinancialRecords")),
    metric(t("totalAmount"), formatMoney(data.total_amount), t("accessibleFlow")),
  ].join("");
  $("#financialFindings").innerHTML = data.findings.length
    ? data.findings
        .map((item) =>
          listItem(
            labelValue(item.finding_type),
            item.description,
            `severity-${item.severity}`,
          ),
        )
        .join("")
    : listItem(t("noFindings"), t("noFinancialFindings"));
  $("#accountLinks").innerHTML = data.account_links?.length
    ? [
        `<h3 class="subsection-title">${escapeHtml(t("accountLinks"))}</h3>`,
        ...data.account_links.map((item) =>
          listItem(
            `${item.source_account} -> ${item.target_account}`,
            `${item.transaction_count} transaction(s) / ${formatMoney(item.total_amount)}`,
          ),
        ),
      ].join("")
    : "";
}

function renderForecast() {
  const data = state.forecast;
  if (!data) return;
  $("#forecastBars").innerHTML = data.hotspots
    .map((item) => {
      const width = Math.max(8, Math.round(item.confidence * 100));
      return `
        <div class="bar-row">
          <header><span>${escapeHtml(item.district)}</span><strong>${item.current_cases} to ${item.projected_7_day_cases}</strong></header>
          <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
          <p>${escapeHtml(item.drivers.join(", "))}</p>
        </div>
      `;
    })
    .join("");
  $("#earlyWarnings").innerHTML = data.early_warnings?.length
    ? [
        `<h3 class="subsection-title">${escapeHtml(t("earlyWarnings"))}</h3>`,
        ...data.early_warnings.map((item) => listItem(t("earlyWarning"), item, "warning-card")),
      ].join("")
    : "";
}

function switchMapProvider(provider) {
  state.mapProvider = provider === "local" ? "leaflet" : provider;
  if (state.mapProvider === "google" && !state.googleMapsKey) {
    state.mapProvider = "leaflet";
    localStorage.setItem("kspMapProvider", state.mapProvider);
    renderCrimeMap();
    $("#googleMapsKey")?.focus();
    renderMapNotice(t("googleKeyRequired"));
    renderTopViewMetrics();
    return;
  }
  localStorage.setItem("kspMapProvider", state.mapProvider);
  renderCrimeMap();
  renderTopViewMetrics();
}

function toggleHeatLayer() {
  state.heatEnabled = !state.heatEnabled;
  renderCrimeMap();
}

function saveGoogleMapsKey() {
  state.googleMapsKey = $("#googleMapsKey").value.trim();
  if (state.googleMapsKey) {
    localStorage.setItem("kspGoogleMapsKey", state.googleMapsKey);
    switchMapProvider("google");
  } else {
    localStorage.removeItem("kspGoogleMapsKey");
    switchMapProvider("leaflet");
  }
}

function renderCrimeMap() {
  const shell = $("#crimeMapShell");
  if (!shell) return;
  if (!$("#map")?.classList.contains("is-active")) {
    renderMapInsights();
    return;
  }
  $("#googleMapsKey").value = state.googleMapsKey;
  $("#localMapBtn").classList.toggle("is-selected", state.mapProvider === "leaflet");
  $("#googleMapBtn").classList.toggle("is-selected", state.mapProvider === "google");
  $("#heatToggleBtn").classList.toggle("is-selected", state.heatEnabled);

  if (state.mapProvider === "google" && state.googleMapsKey) {
    $("#leafletMap").classList.add("is-hidden");
    $("#localMap").classList.add("is-hidden");
    $("#googleMap").classList.remove("is-hidden");
    initGoogleMap()
      .then(() => drawHeatCanvas())
      .catch((error) => {
        renderMapNotice(error.message);
        state.mapProvider = "leaflet";
        localStorage.setItem("kspMapProvider", "leaflet");
        renderCrimeMap();
      });
  } else {
    $("#googleMap").classList.add("is-hidden");
    if (window.L) {
      $("#localMap").classList.add("is-hidden");
      $("#leafletMap").classList.remove("is-hidden");
      initLeafletMap();
      requestAnimationFrame(drawHeatCanvas);
    } else {
      $("#leafletMap").classList.add("is-hidden");
      $("#localMap").classList.remove("is-hidden");
      renderLocalMap();
      requestAnimationFrame(drawHeatCanvas);
    }
  }
  renderMapInsights();
}

function incidentPoints() {
  if (state.advancedCrime?.heatmap_points?.length) {
    return state.advancedCrime.heatmap_points.map((item) => ({
      fir_number: `${item.incident_count} incidents`,
      district: item.district,
      status: item.risk_level,
      sensitivity: item.risk_level === "high" ? "restricted" : "standard",
      case_type: item.top_crime_type,
      time_bucket: item.dominant_time_bucket,
      incident_count: item.incident_count,
      lat: item.latitude,
      lng: item.longitude,
      latitude: item.latitude,
      longitude: item.longitude,
      x: 0,
      y: 0,
      weight: item.weight,
    }));
  }
  const geocoded = (state.cases || []).filter(
    (item) => Number.isFinite(item.latitude) && Number.isFinite(item.longitude),
  );
  if (!geocoded.length) return [];
  const lats = geocoded.map((item) => item.latitude);
  const lngs = geocoded.map((item) => item.longitude);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLng = Math.min(...lngs);
  const maxLng = Math.max(...lngs);
  const latSpan = Math.max(0.01, maxLat - minLat);
  const lngSpan = Math.max(0.01, maxLng - minLng);
  return geocoded.map((item) => {
    const severity = item.sensitivity === "restricted" ? 1.45 : 1;
    return {
      ...item,
      lat: item.latitude,
      lng: item.longitude,
      x: 80 + ((item.longitude - minLng) / lngSpan) * 700,
      y: 440 - ((item.latitude - minLat) / latSpan) * 360,
      weight: severity,
    };
  });
}

function renderLocalMap() {
  const points = incidentPoints();
  if (!points.length) {
    $("#localMapSvg").innerHTML = `<text class="map-label" x="40" y="56">${escapeHtml(t("noOfficialCoordinates"))}</text>`;
    return;
  }
  $("#localMapSvg").innerHTML = `
    ${points.map((point) => `<circle class="incident-point ${point.sensitivity === "restricted" ? "incident-restricted" : "incident-standard"}" cx="${point.x}" cy="${point.y}" r="${point.sensitivity === "restricted" ? 9 : 7}"><title>${escapeHtml(point.fir_number)} ${escapeHtml(point.district)}</title></circle>`).join("")}
  `;
}

function initLeafletMap() {
  if (!window.L) return;
  const points = incidentPoints();
  if (!state.leafletMap) {
    state.leafletMap = L.map("leafletMap", {
      attributionControl: true,
      zoomControl: true,
      preferCanvas: true,
    }).setView(KARNATAKA_CENTER, 7);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(state.leafletMap);
    state.leafletMap.on("move zoom resize", () => drawHeatCanvas());
  }
  requestAnimationFrame(() => {
    state.leafletMap.invalidateSize();
    renderLeafletMarkers(points);
  });
}

function renderLeafletMarkers(points = incidentPoints()) {
  if (!window.L || !state.leafletMap) return;
  state.leafletMarkers.forEach((marker) => marker.remove());
  state.leafletMarkers = points.map((point) =>
    L.circleMarker([point.lat, point.lng], {
      radius: point.sensitivity === "restricted" ? 8 : 6,
      color: "#ffffff",
      weight: 2,
      fillColor: point.sensitivity === "restricted" ? "#b54034" : "#2f6f9f",
      fillOpacity: 0.95,
    })
      .bindPopup(
        `<strong>${escapeHtml(point.fir_number)}</strong><br>${escapeHtml(point.district)}<br>${escapeHtml(point.case_type || point.status)}<br>${escapeHtml(point.time_bucket || "")}`,
      )
      .addTo(state.leafletMap),
  );

  if (points.length) {
    const bounds = L.latLngBounds(points.map((point) => [point.lat, point.lng]));
    state.leafletMap.fitBounds(bounds.pad(0.22), { animate: false, maxZoom: 12 });
  } else {
    state.leafletMap.setView(KARNATAKA_CENTER, 7, { animate: false });
  }
  drawHeatCanvas();
}

function drawHeatCanvas() {
  const canvas = $("#heatCanvas");
  const shell = $("#crimeMapShell");
  if (!canvas || !shell) return;
  const rect = shell.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.round(rect.width * dpr));
  canvas.height = Math.max(1, Math.round(rect.height * dpr));
  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const incidents = incidentPoints();
  renderHeatStatus(incidents);
  if (!state.heatEnabled || !incidents.length) return;

  const points = state.mapProvider === "google" && state.googleMap
    ? googleProjectedPoints(rect)
    : state.mapProvider === "leaflet" && state.leafletMap
      ? leafletProjectedPoints()
    : localProjectedPoints(rect);
  for (const point of points) {
    const radius = 82 * dpr * point.weight;
    const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, radius);
    gradient.addColorStop(0, point.restricted ? "rgba(181,64,52,0.62)" : "rgba(8,127,117,0.52)");
    gradient.addColorStop(0.42, point.restricted ? "rgba(189,121,0,0.34)" : "rgba(47,111,159,0.28)");
    gradient.addColorStop(1, "rgba(8,127,117,0)");
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
    ctx.fill();
  }
}

function renderHeatStatus(points = incidentPoints()) {
  const node = $("#mapStatus");
  if (!node) return;
  const caseCount = state.cases?.length || 0;
  if (!state.heatEnabled) {
    node.classList.remove("is-hidden");
    node.innerHTML = `<strong>${escapeHtml(t("heatLayerHidden"))}</strong><span>${escapeHtml(t("heatLayerHiddenBody"))}</span>`;
    return;
  }
  if (!caseCount) {
    node.classList.remove("is-hidden");
    node.innerHTML = `<strong>${escapeHtml(t("noHeatData"))}</strong><span>${escapeHtml(t("noOfficialRecordsLoaded"))}</span>`;
    return;
  }
  if (!points.length) {
    node.classList.remove("is-hidden");
    node.innerHTML = `<strong>${escapeHtml(t("noOfficialCoordinatesTitle"))}</strong><span>${caseCount} ${escapeHtml(t("recordsNoCoordinates"))}</span>`;
    return;
  }
  node.classList.add("is-hidden");
  node.textContent = "";
}

function localProjectedPoints(rect) {
  const dpr = window.devicePixelRatio || 1;
  const points = incidentPoints();
  const lats = points.map((item) => item.lat).filter(Number.isFinite);
  const lngs = points.map((item) => item.lng).filter(Number.isFinite);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLng = Math.min(...lngs);
  const maxLng = Math.max(...lngs);
  const latSpan = Math.max(0.01, maxLat - minLat);
  const lngSpan = Math.max(0.01, maxLng - minLng);
  return points.map((point) => {
    const x = point.x ? point.x : 80 + ((point.lng - minLng) / lngSpan) * 700;
    const y = point.y ? point.y : 440 - ((point.lat - minLat) / latSpan) * 360;
    return {
      x: (x / 860) * rect.width * dpr,
      y: (y / 520) * rect.height * dpr,
      weight: point.weight,
      restricted: point.sensitivity === "restricted",
    };
  });
}

function leafletProjectedPoints() {
  if (!state.leafletMap) return [];
  const dpr = window.devicePixelRatio || 1;
  return incidentPoints().map((point) => {
    const projected = state.leafletMap.latLngToContainerPoint([point.lat, point.lng]);
    return {
      x: projected.x * dpr,
      y: projected.y * dpr,
      weight: point.weight,
      restricted: point.sensitivity === "restricted",
    };
  });
}

function googleProjectedPoints(rect) {
  const projection = state.googleMap?.getProjection?.();
  const bounds = state.googleMap?.getBounds?.();
  if (!projection || !bounds || !window.google?.maps) return localProjectedPoints(rect);
  const topRight = projection.fromLatLngToPoint(bounds.getNorthEast());
  const bottomLeft = projection.fromLatLngToPoint(bounds.getSouthWest());
  const zoomScale = 2 ** state.googleMap.getZoom();
  const dpr = window.devicePixelRatio || 1;
  return incidentPoints().map((point) => {
    const world = projection.fromLatLngToPoint(new google.maps.LatLng(point.lat, point.lng));
    return {
      x: (world.x - bottomLeft.x) * zoomScale * dpr,
      y: (world.y - topRight.y) * zoomScale * dpr,
      weight: point.weight,
      restricted: point.sensitivity === "restricted",
    };
  });
}

async function initGoogleMap() {
  if (!state.googleMapsKey) throw new Error("Add a Google Maps API key to use Google Maps mode.");
  await loadGoogleMapsScript(state.googleMapsKey);
  if (!state.googleMap) {
    const points = incidentPoints();
    const center = points.length ? { lat: points[0].lat, lng: points[0].lng } : { lat: 0, lng: 0 };
    state.googleMap = new google.maps.Map($("#googleMap"), {
      center,
      zoom: 7,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      styles: [
        { featureType: "poi", stylers: [{ visibility: "off" }] },
        { featureType: "administrative", elementType: "labels.text.fill", stylers: [{ color: "#33413d" }] },
      ],
    });
    state.googleMap.addListener("bounds_changed", () => drawHeatCanvas());
  }
  addGoogleMarkers();
}

function addGoogleMarkers() {
  if (!window.google?.maps || !state.googleMap) return;
  state.googleMarkers.forEach((marker) => marker.setMap(null));
  state.googleMarkers = incidentPoints().map((point) => new google.maps.Marker({
    position: { lat: point.lat, lng: point.lng },
    map: state.googleMap,
    title: `${point.fir_number} / ${point.district}`,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: point.sensitivity === "restricted" ? 7 : 6,
      fillColor: point.sensitivity === "restricted" ? "#b54034" : "#2f6f9f",
      fillOpacity: 0.95,
      strokeColor: "#ffffff",
      strokeWeight: 2,
    },
  }));
}

function loadGoogleMapsScript(key) {
  if (window.google?.maps) return Promise.resolve();
  if (window.__googleMapsLoading) return window.__googleMapsLoading;
  window.__googleMapsLoading = new Promise((resolve, reject) => {
    window.__kspGoogleMapsReady = () => resolve();
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&callback=__kspGoogleMapsReady`;
    script.async = true;
    script.defer = true;
    script.onerror = () => reject(new Error("Google Maps could not load. Check the API key and network access."));
    document.head.appendChild(script);
  });
  return window.__googleMapsLoading;
}

function renderMapInsights() {
  const cases = state.cases || [];
  const advanced = state.advancedCrime;
  if (advanced?.imported_count) {
    const riskRows = (advanced.risk_areas || [])
      .slice(0, 8)
      .map((item) =>
        listItem(
          `${item.district} / ${item.crime_type}`,
          `${t("riskScore")}: ${item.score}. ${item.drivers.join(", ")}`,
          `severity-${item.risk_level}`,
        ),
      );
    const alertRows = (advanced.emerging_trend_alerts || [])
      .slice(0, 5)
      .map((item) => listItem(t("earlyWarning"), item.explanation, `severity-${item.severity}`));
    const totals = [
      listItem(t("mlIncidents"), `${advanced.imported_count} imported / ${advanced.geocoded_count} geocoded.`),
      listItem(t("heatMap"), `${advanced.heatmap_points.length} aggregate heatmap cluster(s).`),
    ];
    $("#mapInsights").innerHTML = [...totals, ...riskRows, ...alertRows].join("");
    return;
  }
  const geocoded = cases.filter((item) => Number.isFinite(item.latitude) && Number.isFinite(item.longitude));
  const byDistrict = cases.reduce((acc, item) => {
    acc[item.district] = (acc[item.district] || 0) + 1;
    return acc;
  }, {});
  const rows = Object.entries(byDistrict)
    .sort((a, b) => b[1] - a[1])
    .map(([district, count]) => {
      const restricted = cases.filter((item) => item.district === district && item.sensitivity === "restricted").length;
      const mapped = cases.filter((item) => item.district === district && Number.isFinite(item.latitude) && Number.isFinite(item.longitude)).length;
      return listItem(district, `${count} case(s), ${restricted} restricted, ${mapped} geocoded.`);
    });
  const extra = [
    listItem(t("officialCoordinates"), `${geocoded.length} / ${cases.length} ${t("authorizedGeocoded")}`),
    listItem(t("heatMap"), state.heatEnabled ? t("heatLayerActive") : t("heatLayerHidden")),
  ];
  $("#mapInsights").innerHTML = [...rows, ...extra].join("");
}

function renderMapNotice(message) {
  $("#mapInsights").innerHTML = listItem(t("mapNotice"), message);
}

async function loadUsers() {
  if (!isSuperAdmin()) {
    renderPermission("#userList", "Super admin access is required.");
    return;
  }
  try {
    state.users = await api("/admin/users");
    renderUsers();
    renderAdminActivityPrompt();
  } catch (error) {
    renderPermission("#userList", error.message);
  }
}

function renderUsers() {
  const roles = ["viewer", "analyst", "policymaker", "investigator", "supervisor", "super_admin"];
  $("#userList").innerHTML = state.users.length
    ? state.users
        .map((user) => `
          <article class="list-item admin-user-card">
            <header>
              <strong>${escapeHtml(user.full_name)}</strong>
              <span class="badge">${escapeHtml(labelValue(user.role))}</span>
            </header>
            <p>${escapeHtml(user.username)} / ${escapeHtml(user.district)} / ${user.is_active ? escapeHtml(t("active")) : escapeHtml(t("disabled"))}</p>
            <div class="admin-user-actions">
              <select data-admin-role="${escapeHtml(user.id)}">
                ${roles.map((role) => `<option value="${role}" ${role === user.role ? "selected" : ""}>${escapeHtml(labelValue(role))}</option>`).join("")}
              </select>
              <input data-admin-district="${escapeHtml(user.id)}" value="${escapeHtml(user.district)}" aria-label="District for ${escapeHtml(user.username)}" />
              <label class="toggle-line">
                <input type="checkbox" data-admin-active="${escapeHtml(user.id)}" ${user.is_active ? "checked" : ""} />
                <span>${escapeHtml(t("active"))}</span>
              </label>
              <button class="icon-button" title="Save user" aria-label="Save user" data-admin-save="${escapeHtml(user.id)}"><i data-lucide="check"></i></button>
              <button class="icon-button" title="View activity" aria-label="View activity" data-admin-activity="${escapeHtml(user.id)}"><i data-lucide="activity"></i></button>
              <button class="icon-button" title="Reset password" aria-label="Reset password" data-admin-reset="${escapeHtml(user.id)}"><i data-lucide="key-round"></i></button>
              <button class="icon-button danger-button" title="Delete user" aria-label="Delete user" data-admin-delete="${escapeHtml(user.id)}"><i data-lucide="trash-2"></i></button>
            </div>
          </article>
        `)
        .join("")
    : listItem(t("noUsers"), t("noAuthorizedAccounts"));

  $$("[data-admin-save]").forEach((button) => {
    button.addEventListener("click", () => updateAdminUser(button.dataset.adminSave));
  });
  $$("[data-admin-reset]").forEach((button) => {
    button.addEventListener("click", () => resetAdminPassword(button.dataset.adminReset));
  });
  $$("[data-admin-activity]").forEach((button) => {
    button.addEventListener("click", () => loadAdminUserActivity(button.dataset.adminActivity));
  });
  $$("[data-admin-delete]").forEach((button) => {
    button.addEventListener("click", () => deleteAdminUser(button.dataset.adminDelete));
  });
  iconRefresh();
}

async function createAdminUser(event) {
  event.preventDefault();
  setText("#adminResult", "");
  const payload = {
    username: $("#adminUsername").value.trim(),
    password: $("#adminPassword").value,
    full_name: $("#adminFullName").value.trim(),
    role: $("#adminRole").value,
    district: $("#adminDistrict").value.trim(),
    is_active: true,
  };
  if (!payload.username || !payload.password || !payload.full_name || !payload.district) {
    setText("#adminResult", t("adminRequiredFields"));
    return;
  }
  try {
    const created = await api("/admin/users", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    $("#createUserForm").reset();
    setText("#adminResult", `${t("created")} ${created.username}.`);
    await loadUsers();
  } catch (error) {
    setText("#adminResult", error.message);
  }
}

async function updateAdminUser(userId) {
  const role = $(`[data-admin-role="${cssEscape(userId)}"]`)?.value;
  const district = $(`[data-admin-district="${cssEscape(userId)}"]`)?.value.trim();
  const active = $(`[data-admin-active="${cssEscape(userId)}"]`)?.checked;
  if (!role || !district) {
    setText("#adminResult", "Role and district are required for user updates.");
    return;
  }
  try {
    const updated = await api(`/admin/users/${encodeURIComponent(userId)}`, {
      method: "PATCH",
      body: JSON.stringify({ role, district, is_active: Boolean(active) }),
    });
    setText("#adminResult", `Updated ${updated.username}.`);
    await loadUsers();
  } catch (error) {
    setText("#adminResult", error.message);
  }
}

async function loadAdminUserActivity(userId) {
  const user = state.users.find((item) => item.id === userId);
  try {
    const payload = await api(`/admin/users/${encodeURIComponent(userId)}/activity?limit=40`);
    renderAdminActivity(payload);
    setText("#adminResult", `${t("activityLoaded")} ${user?.username || payload.user?.username || ""}.`);
  } catch (error) {
    renderPermission("#adminActivity", error.message);
    setText("#adminResult", error.message);
  }
}

function renderAdminActivity(payload) {
  const user = payload?.user;
  const events = payload?.events || [];
  const title = user ? `${user.username} / ${labelValue(user.role)} / ${user.is_active ? t("active") : t("disabled")}` : t("userActivity");
  $("#adminActivity").innerHTML = `
    ${listItem(t("selectedUser"), title)}
    ${events.length
      ? events
          .map((event) => {
            const detail = formatActivityDetail(event.detail);
            const body = [
              `${event.status} / ${event.resource_type} / ${formatDate(event.created_at)}`,
              event.actor_username ? `${t("actor")}: ${event.actor_username}` : "",
              event.resource_id ? `${t("resource")}: ${event.resource_id}` : "",
              detail,
            ].filter(Boolean).join("\n");
            return listItem(event.action, body, "admin-activity-event");
          })
          .join("")
      : listItem(t("noActivityEvents"), t("noActivityEventsBody"))}
  `;
  iconRefresh();
}

function renderAdminActivityPrompt() {
  const panel = $("#adminActivity");
  if (!panel || panel.innerHTML.trim()) return;
  panel.innerHTML = listItem(t("userActivity"), t("selectUserActivity"));
}

function formatActivityDetail(detail) {
  if (!detail || typeof detail !== "object") return "";
  return Object.entries(detail)
    .slice(0, 5)
    .map(([key, value]) => `${labelValue(key)}: ${typeof value === "object" ? JSON.stringify(value) : value}`)
    .join(" / ");
}

async function deleteAdminUser(userId) {
  const user = state.users.find((item) => item.id === userId);
  const username = user?.username || "this user";
  if (!window.confirm(`${t("deleteUserConfirm")} ${username}?`)) return;
  try {
    const result = await api(`/admin/users/${encodeURIComponent(userId)}`, { method: "DELETE" });
    setText("#adminResult", `${t("deleted")} ${result.username} (${labelValue(result.status)}).`);
    $("#adminActivity").innerHTML = listItem(t("userActivity"), t("selectUserActivity"));
    await loadUsers();
  } catch (error) {
    setText("#adminResult", error.message);
  }
}

async function resetAdminPassword(userId) {
  const password = window.prompt(t("passwordPrompt"));
  if (password === null) return;
  if (password.length < 12) {
    setText("#adminResult", t("passwordTooShort"));
    return;
  }
  try {
    await api(`/admin/users/${encodeURIComponent(userId)}/reset-password`, {
      method: "POST",
      body: JSON.stringify({ password }),
    });
    setText("#adminResult", t("passwordResetComplete"));
  } catch (error) {
    setText("#adminResult", error.message);
  }
}

async function loadRateLimitAlerts(showErrors = true) {
  if (!isSuperAdmin()) return;
  try {
    state.rateLimitAlerts = await api("/admin/rate-limit-alerts?limit=25");
    renderRateLimitAlerts();
  } catch (error) {
    if (showErrors) renderPermission("#rateLimitAlerts", error.message);
  }
}

function renderRateLimitAlerts() {
  const count = state.rateLimitAlerts.length;
  setText("#rateAlertCount", `${count} ${t("open")}`);
  $("#rateLimitAlerts").innerHTML = count
    ? state.rateLimitAlerts
        .map((alert) => {
          const actor = alert.actor_username
            ? `${alert.actor_username} / ${alert.actor_role}`
            : `${t("unauthenticatedIp")} ${alert.client_ip || "unknown"}`;
          return `
            <article class="list-item rate-alert-card">
              <header>
                <strong>${escapeHtml(actor)}</strong>
                <button class="icon-button" title="Acknowledge alert" aria-label="Acknowledge alert" data-rate-alert-ack="${alert.id}"><i data-lucide="check"></i></button>
              </header>
              <p>${escapeHtml(alert.method)} ${escapeHtml(alert.path)} ${escapeHtml(t("breachedLimit"))} ${alert.limit_per_minute}/minute ${escapeHtml(t("withRequests"))} ${alert.request_count}.</p>
              <div class="rate-alert-meta">
                <span>${escapeHtml(formatDate(alert.created_at))}</span>
                <span>${escapeHtml(t("client"))} ${escapeHtml(alert.client_ip || "unknown")}</span>
                <span>${escapeHtml(t("request"))} ${escapeHtml(alert.request_id || "n/a")}</span>
              </div>
            </article>
          `;
        })
        .join("")
    : listItem(t("noOpenBreaches"), t("breachesAppearHere"));

  $$("[data-rate-alert-ack]").forEach((button) => {
    button.addEventListener("click", () => acknowledgeRateLimitAlert(button.dataset.rateAlertAck));
  });
  iconRefresh();
}

async function acknowledgeRateLimitAlert(alertId) {
  try {
    await api(`/admin/rate-limit-alerts/${encodeURIComponent(alertId)}/acknowledge`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    await loadRateLimitAlerts(false);
  } catch (error) {
    renderPermission("#rateLimitAlerts", error.message);
  }
}

function startRateAlertPolling() {
  if (state.rateAlertPoller) return;
  state.rateAlertPoller = window.setInterval(() => {
    if (state.token && isSuperAdmin()) {
      loadRateLimitAlerts(false);
    }
  }, 15000);
}

function stopRateAlertPolling() {
  if (!state.rateAlertPoller) return;
  window.clearInterval(state.rateAlertPoller);
  state.rateAlertPoller = null;
}

function renderHotspots() {
  const hotspots = state.forecast?.hotspots || [];
  $("#hotspotList").innerHTML = hotspots.length
    ? hotspots
        .map((item) =>
          listItem(
            item.district,
            `${item.current_cases} ${t("currentCases")}, ${item.projected_7_day_cases} ${t("projectedPlanning")}.`,
          ),
        )
        .join("")
    : listItem(t("pending"), t("forecastPending"));
}

async function createConversation() {
  try {
    const conversation = await api("/conversations", {
      method: "POST",
      body: JSON.stringify({ title: "Investigation chat" }),
    });
    state.conversationId = conversation.id;
    $("#conversationFeed").innerHTML = "";
  } catch (error) {
    addMessage("assistant", error.message);
  }
}

async function handleQuery(event) {
  event.preventDefault();
  const query = $("#queryInput").value.trim();
  if (!query) return;
  await submitQueryText(query);
}

async function handleGlobalSearch(event) {
  event.preventDefault();
  const input = $("#globalSearchInput");
  const query = input?.value.trim() || "";
  setPanel("command");
  if (!query) {
    $("#queryInput")?.focus();
    return;
  }
  input.value = "";
  await submitQueryText(query);
}

async function submitQueryText(query) {
  $("#queryInput").value = "";
  let pendingId = null;
  try {
    if (!state.conversationId) {
      const conversation = await api("/conversations", {
        method: "POST",
        body: JSON.stringify({ title: "Investigation chat" }),
      });
      state.conversationId = conversation.id;
      $("#conversationFeed").innerHTML = "";
    }
    addMessage("user", query);
    pendingId = addMessage("assistant", t("analyzingCrimeData"), null, { pending: true });
    const exchange = await api(`/conversations/${state.conversationId}/messages`, {
      method: "POST",
      body: JSON.stringify({ query, language: state.queryLanguage }),
    });
    removeMessage(pendingId);
    addMessage("assistant", exchange.assistant_message.content, exchange.intelligence);
    renderLiveContext(exchange.intelligence, query);
  } catch (error) {
    removeMessage(pendingId);
    addMessage("assistant", error.message);
  }
}

function launchTaskPrompt(prompt) {
  setPanel("command");
  $("#queryInput").value = prompt;
  window.setTimeout(() => {
    $("#queryForm").requestSubmit();
  }, 0);
}

function startVoiceQuery() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    addMessage("assistant", t("voiceUnsupported"));
    return;
  }
  const recognition = new Recognition();
  recognition.lang = state.queryLanguage === "kn" ? "kn-IN" : "en-IN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  $("#voiceBtn")?.classList.add("is-listening");
  recognition.onresult = (event) => {
    const transcript = event.results?.[0]?.[0]?.transcript || "";
    $("#queryInput").value = transcript;
  };
  recognition.onerror = () => addMessage("assistant", t("voiceFailed"));
  recognition.onend = () => $("#voiceBtn")?.classList.remove("is-listening");
  recognition.start();
}

function parseMarkdownToHtml(text) {
  if (!text) return "";
  let html = String(text);
  // Blockquotes
  html = html.replace(/^&gt;\s?(.+)$/gm, '<blockquote class="md-blockquote">$1</blockquote>');
  // H3
  html = html.replace(/^###\s+(.+)$/gm, '<h3 class="md-h3">$1</h3>');
  // H2
  html = html.replace(/^##\s+(.+)$/gm, '<h2 class="md-h2">$1</h2>');
  // H1
  html = html.replace(/^#\s+(.+)$/gm, '<h1 class="md-h1">$1</h1>');
  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // Italic
  html = html.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="md-code">$1</code>');
  // Unordered lists
  html = html.replace(/((?:^[-*]\s.+(?:\n|$))+)/gm, (block) => {
    const items = block.trim().split(/\n/).map(line => `<li>${line.replace(/^[-*]\s/, '')}</li>`).join('');
    return `<ul class="md-list">${items}</ul>`;
  });
  // Line breaks for non-block elements
  html = html.replace(/(?<!>)\n(?!\n|<)/g, '<br>');
  // Remove consecutive empty lines
  html = html.replace(/(\n){3,}/g, '\n\n');
  return html;
}

function formatAssistantText(content, intelligence = null) {
  const sections = parseAssistantSections(content);
  const directAnswer = sections["Direct Answer"] || sections["ಉತ್ತರ"];
  if (directAnswer) {
    const metaOrder = [
      "Intent",
      "Selected Module",
      "Evidence Sources",
      "Confidence",
      "Reasoning",
      "Suggested Follow-up Questions",
      "ಉದ್ದೇಶ",
      "ಆಯ್ಕೆ ಮಾಡಿದ ಘಟಕ",
      "ಮೂಲ ದಾಖಲೆ",
      "ವಿಶ್ವಾಸ",
      "ಕಾರಣ",
      "ಮುಂದಿನ ಪ್ರಶ್ನೆಗಳು",
    ];
    const metaHtml = metaOrder
      .filter((label) => sections[label])
      .map((label) => `
        <div class="assistant-section-row">
          <b>${escapeHtml(label)}</b>
          <span>${escapeHtml(sections[label]).replaceAll("\n", "<br>")}</span>
        </div>
      `)
      .join("");
    return `
      <article class="intelligence-answer-card">
        <header>
          <span class="assistant-orb small"><i data-lucide="${assistantIntentIcon(sections)}"></i></span>
          <div>
            <p>${escapeHtml(sections.Intent || sections["ಉದ್ದೇಶ"] || "Crime Intelligence")}</p>
            <h3>${escapeHtml(sections["Selected Module"] || sections["ಆಯ್ಕೆ ಮಾಡಿದ ಘಟಕ"] || intelligence?.selected_module || "Evidence-bound answer")}</h3>
          </div>
          ${sections.Confidence || intelligence?.confidence ? `<b>${escapeHtml(sections.Confidence || intelligence.confidence)}</b>` : ""}
        </header>
        <div class="assistant-direct-answer">${parseMarkdownToHtml(escapeHtml(directAnswer))}</div>
        ${renderAssistantCardPreview(sections, intelligence)}
        ${renderAssistantCardActions(sections, intelligence)}
      </article>
      ${metaHtml ? `
        <details class="assistant-response-details">
          <summary>${escapeHtml(t("answerSupport"))}</summary>
          <div>${metaHtml}</div>
        </details>
      ` : ""}
    `;
  }
  const plainChat =
    intelligence?.presentation?.render_evidence === false &&
    intelligence?.presentation?.render_actions === false;
  const bodyHtml = parseMarkdownToHtml(escapeHtml(String(content ?? "")));
  if (plainChat) {
    return `<div class="md-body">${bodyHtml}</div>`;
  }
  // Detect if content has markdown structure (headers, bullets)
  const hasMarkdown = /^#{1,3}\s|^[-*]\s|\*\*|```/m.test(String(content ?? ""));
  return `
    <article class="intelligence-answer-card simple-card${hasMarkdown ? " markdown-card" : ""}">
      <header>
        <span class="assistant-orb small"><i data-lucide="shield-check"></i></span>
        <div>
          <p>KSP AI</p>
          <h3>${hasMarkdown ? "Intelligence Analysis" : "Crime intelligence response"}</h3>
        </div>
      </header>
      <div class="md-body">${bodyHtml}</div>
      ${renderAssistantCardActions(sections, intelligence)}
    </article>
  `;
}

function parseMarkdownToHtml(text) {

function clearConversationView() {
  $("#conversationFeed").innerHTML = "";
  state.conversationId = null;
  resetLiveContext();
  $("#queryInput")?.focus();
}

function launchAssistantChip(template) {
  setPanel("command");
  const input = $("#queryInput");
  if (!input) return;
  const needsDetail = /\s$/.test(template);
  input.value = needsDetail ? template : template;
  input.focus();
  if (!needsDetail && template.length > 10) {
    window.setTimeout(() => $("#queryForm").requestSubmit(), 0);
  }
}

function handleAssistantActionClick(event) {
  const contextButton = event.target.closest("[data-context-query]");
  if (contextButton) {
    const subject = $("#contextSubject")?.textContent?.trim();
    if (!subject || subject === "No active investigation selected") return;
    const query = contextButton.dataset.contextQuery.replace("{subject}", subject);
    submitQueryText(query);
    return;
  }
  const assistantButton = event.target.closest("[data-assistant-query]");
  if (assistantButton) {
    submitQueryText(assistantButton.dataset.assistantQuery);
  }
}

function resetLiveContext() {
  setText("#contextSubject", "No active investigation selected");
  ["#contextRiskScore", "#contextCurrentFir", "#contextLinkedCases", "#contextNetworkSize", "#contextAssociates", "#contextFinancialExposure", "#contextCommunity", "#contextThreatLevel"].forEach((selector) => {
    setText(selector, "--");
  });
}

function renderLiveContext(intelligence, query = "") {
  const subject = extractPrimarySubjectFromIntelligence(intelligence, query);
  const sources = Array.isArray(intelligence?.sources) ? intelligence.sources : [];
  const node = findNetworkNodeBySubject(subject);
  const networkStats = node ? calculateNodeNetworkStats(node.id) : { neighbors: 0, links: 0 };
  const linkedCases = new Set([
    ...sources.map((source) => source.fir_number || source.case_id).filter(Boolean),
    ...(node?.metadata?.cases || []).map((item) => item.fir_number || item.case_id).filter(Boolean),
    ...(node?.metadata?.linked_cases || []).map((item) => item.fir_number || item.case_id).filter(Boolean),
  ]).size || Number(intelligence?.visible_case_count || 0);
  const rawRisk = Number(
    intelligence?.risk_score ||
    node?.risk_score ||
    node?.metadata?.risk_score ||
    (linkedCases >= 4 ? 82 : linkedCases >= 2 ? 64 : 0),
  );
  const riskScore = rawRisk ? `${Math.min(100, Math.round(rawRisk))}/100` : "--";
  const financialExposure = estimateFinancialExposure(subject, node);
  const community = node?.community || node?.metadata?.community || node?.metadata?.community_id || "--";
  const threatLevel = rawRisk >= 80 ? "High" : rawRisk >= 55 ? "Medium" : rawRisk > 0 ? "Low" : "--";
  const currentFir = sources.find((source) => source.fir_number || source.case_id);

  setText("#contextSubject", subject || "No active investigation selected");
  setText("#contextRiskScore", riskScore);
  setText("#contextCurrentFir", currentFir ? shorten(currentFir.fir_number || currentFir.case_id, 18) : "--");
  setText("#contextLinkedCases", linkedCases ? formatCount(linkedCases) : "--");
  setText("#contextNetworkSize", networkStats.links ? formatCount(networkStats.links) : "--");
  setText("#contextAssociates", networkStats.neighbors ? formatCount(networkStats.neighbors) : "--");
  setText("#contextFinancialExposure", financialExposure);
  setText("#contextCommunity", String(community));
  setText("#contextThreatLevel", threatLevel);
}

function extractPrimarySubjectFromIntelligence(intelligence, query = "") {
  const entities = intelligence?.extracted_entities || intelligence?.entities || intelligence?.query_analysis?.entities || {};
  const entityCandidates = [
    entities.suspect_name,
    entities.person_name,
    entities.person,
    entities.name,
    entities.accused_name,
    entities.victim_name,
    entities.complainant_name,
    entities.fir_number,
    entities.case_number,
  ].flat().filter(Boolean);
  if (entityCandidates.length) return String(entityCandidates[0]);
  const source = (intelligence?.sources || []).find(Boolean);
  if (source) {
    return source.suspect_name || source.accused_name || source.victim_name || source.complainant_name || source.fir_number || source.case_id || "";
  }
  const nameMatch = String(query).match(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}|[A-Z]\d+|[A-Z]{2,}-\d{4}-\d{4})\b/);
  if (nameMatch) return nameMatch[1];
  const normalized = intelligence?.query_analysis?.normalized_query || query;
  return normalized ? shorten(normalized, 44) : "";
}

function findNetworkNodeBySubject(subject) {
  const normalized = String(subject || "").trim().toLowerCase();
  if (!normalized) return null;
  return (state.network?.nodes || []).find((node) => {
    const labels = [
      node.id,
      node.label,
      node.metadata?.suspect_name,
      node.metadata?.account_holder,
      node.metadata?.fir_number,
      node.metadata?.case_number,
    ].filter(Boolean).map((value) => String(value).toLowerCase());
    return labels.some((label) => label === normalized || label.includes(normalized) || normalized.includes(label));
  }) || null;
}

function calculateNodeNetworkStats(nodeId) {
  const neighbors = new Set();
  let links = 0;
  (state.network?.links || []).forEach((link) => {
    if (link.source === nodeId || link.target === nodeId) {
      links += 1;
      neighbors.add(link.source === nodeId ? link.target : link.source);
    }
  });
  return { neighbors: neighbors.size, links };
}

function estimateFinancialExposure(subject, node) {
  const accounts = node?.metadata?.accounts || [];
  const normalized = String(subject || "").toLowerCase();
  let total = 0;
  (state.financial?.account_links || []).forEach((link) => {
    const haystack = [link.source_account, link.target_account, link.source_holder, link.target_holder].filter(Boolean).join(" ").toLowerCase();
    if ((normalized && haystack.includes(normalized)) || accounts.some((account) => haystack.includes(String(account).toLowerCase()))) {
      total += Number(link.total_amount || 0);
    }
  });
  return total ? formatMoney(total) : "--";
}

function addMessage(role, content, intelligence = null, options = {}) {
  const id = `msg-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const sourceEvidence = Array.isArray(intelligence) ? { sources: intelligence } : intelligence;
  const evidenceHtml = role === "assistant" && sourceEvidence ? renderAssistantEvidence(sourceEvidence) : "";
  const pendingHtml = options.pending ? '<span class="typing-dots"><b></b><b></b><b></b></span>' : "";
  const avatar = role === "assistant" ? '<div class="message-avatar"><i data-lucide="shield-check"></i></div>' : "";
  const bodyHtml = role === "assistant"
    ? formatAssistantText(content, sourceEvidence)
    : `<p>${escapeHtml(content).replaceAll("\n", "<br>")}</p>`;
  $("#conversationFeed").insertAdjacentHTML(
    "beforeend",
    `<article class="message ${role} ${options.pending ? "is-pending" : ""}" id="${id}">
      ${avatar}
      <div class="message-body">
        <div class="assistant-answer">${bodyHtml}${pendingHtml}</div>
        ${evidenceHtml}
      </div>
    </article>`,
  );
  iconRefresh();
  scrollConversationToMessage(id, role === "assistant" && sourceEvidence && !options.pending ? "start" : "end");
  return id;
}

function scrollConversationToMessage(messageId, align = "end") {
  const feed = $("#conversationFeed");
  const message = document.getElementById(messageId);
  if (!feed || !message) return;
  window.requestAnimationFrame(() => {
    if (align === "start") {
      feed.scrollTop = Math.max(0, message.offsetTop - feed.offsetTop - 8);
      feed.scrollIntoView({ block: "start", behavior: "smooth" });
      return;
    }
    feed.scrollTop = feed.scrollHeight;
  });
}

function removeMessage(messageId) {
  if (!messageId) return;
  const node = document.getElementById(messageId);
  if (node) node.remove();
}

function formatAssistantText(content, intelligence = null) {
  const sections = parseAssistantSections(content);
  const directAnswer = sections["Direct Answer"] || sections["ಉತ್ತರ"];
  if (directAnswer) {
    const metaOrder = [
      "Intent",
      "Selected Module",
      "Evidence Sources",
      "Confidence",
      "Reasoning",
      "Suggested Follow-up Questions",
      "ಉದ್ದೇಶ",
      "ಆಯ್ಕೆ ಮಾಡಿದ ಘಟಕ",
      "ಮೂಲ ದಾಖಲೆ",
      "ವಿಶ್ವಾಸ",
      "ಕಾರಣ",
      "ಮುಂದಿನ ಪ್ರಶ್ನೆಗಳು",
    ];
    const metaHtml = metaOrder
      .filter((label) => sections[label])
      .map((label) => `
        <div class="assistant-section-row">
          <b>${escapeHtml(label)}</b>
          <span>${escapeHtml(sections[label]).replaceAll("\n", "<br>")}</span>
        </div>
      `)
      .join("");
    return `
      <article class="intelligence-answer-card">
        <header>
          <span class="assistant-orb small"><i data-lucide="${assistantIntentIcon(sections)}"></i></span>
          <div>
            <p>${escapeHtml(sections.Intent || sections["à²‰à²¦à³à²¦à³‡à²¶"] || "Crime Intelligence")}</p>
            <h3>${escapeHtml(sections["Selected Module"] || sections["à²†à²¯à³à²•à³† à²®à²¾à²¡à²¿à²¦ à²˜à²Ÿà²•"] || intelligence?.selected_module || "Evidence-bound answer")}</h3>
          </div>
          ${sections.Confidence || intelligence?.confidence ? `<b>${escapeHtml(sections.Confidence || intelligence.confidence)}</b>` : ""}
        </header>
        <div class="assistant-direct-answer">${escapeHtml(directAnswer).replaceAll("\n", "<br>")}</div>
        ${renderAssistantCardPreview(sections, intelligence)}
        ${renderAssistantCardActions(sections, intelligence)}
      </article>
      ${metaHtml ? `
        <details class="assistant-response-details">
          <summary>${escapeHtml(t("answerSupport"))}</summary>
          <div>${metaHtml}</div>
        </details>
      ` : ""}
    `;
  }
  const paragraphs = String(content ?? "")
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .filter(Boolean);
  if (!paragraphs.length) return "<p></p>";
  const plainChat =
    intelligence?.presentation?.render_evidence === false &&
    intelligence?.presentation?.render_actions === false;
  if (plainChat) {
    return paragraphs.map((part) => `<p>${escapeHtml(part).replaceAll("\n", "<br>")}</p>`).join("");
  }
  return `
    <article class="intelligence-answer-card simple-card">
      <header>
        <span class="assistant-orb small"><i data-lucide="shield-check"></i></span>
        <div>
          <p>KSP AI</p>
          <h3>Crime intelligence response</h3>
        </div>
      </header>
      ${paragraphs.map((part) => `<p>${escapeHtml(part).replaceAll("\n", "<br>")}</p>`).join("")}
      ${renderAssistantCardActions(sections, intelligence)}
    </article>
  `;
}

function assistantIntentIcon(sections) {
  const intent = String(sections.Intent || "").toLowerCase();
  const module = String(sections["Selected Module"] || "").toLowerCase();
  if (intent.includes("network") || module.includes("network")) return "git-fork";
  if (intent.includes("financial") || module.includes("financial") || intent.includes("money")) return "indian-rupee";
  if (intent.includes("hotspot") || intent.includes("forecast") || module.includes("forecast")) return "map-pinned";
  if (intent.includes("profile") || intent.includes("suspect")) return "user-search";
  if (intent.includes("audit")) return "fingerprint";
  if (intent.includes("fir") || intent.includes("case")) return "folder-kanban";
  return "shield-check";
}

function renderAssistantCardPreview(sections, intelligence) {
  const sources = Array.isArray(intelligence?.sources) ? intelligence.sources : [];
  const source = sources[0] || {};
  const chips = [
    sections["Evidence Sources"] || source.fir_number || source.case_id,
    sections.Confidence || intelligence?.confidence,
    sources.length ? `${sources.length} source record(s)` : "",
    intelligence?.visible_case_count ? `${formatCount(intelligence.visible_case_count)} visible case(s)` : "",
  ].filter(Boolean);
  if (!chips.length) return "";
  return `
    <div class="intelligence-preview-grid">
      ${chips.slice(0, 4).map((chip) => `<span>${escapeHtml(shorten(chip, 72))}</span>`).join("")}
    </div>
  `;
}

function renderAssistantCardActions(sections, intelligence) {
  if (!intelligence) return "";
  if (intelligence?.presentation?.render_actions === false) return "";
  const configured = Array.isArray(intelligence?.presentation?.suggested_actions)
    ? intelligence.presentation.suggested_actions.filter(isActionableAssistantQuery)
    : [];
  if (configured.length) {
    return `
      <div class="assistant-card-actions">
        ${configured.slice(0, 3).map((query) => `<button type="button" data-assistant-query="${escapeHtml(query)}">${escapeHtml(shorten(query, 42))}</button>`).join("")}
      </div>
    `;
  }
  const subject = extractPrimarySubjectFromIntelligence(intelligence, sections["Direct Answer"] || "");
  const safeSubject = subject ? String(subject) : "";
  const actions = [
    ["Open Profile", safeSubject ? `Create suspect profile for ${safeSubject}` : ""],
    ["Show Network", safeSubject ? `Show criminal network for ${safeSubject}` : "Show criminal network analysis"],
    ["Show Timeline", safeSubject ? `Build investigation timeline for ${safeSubject}` : ""],
    ["Money Trail", safeSubject ? `Show money trail for ${safeSubject}` : "Show financial fraud money trail"],
  ].filter(([, query]) => query);
  if (!actions.length) return "";
  return `
    <div class="assistant-card-actions">
      ${actions.map(([label, query]) => `<button type="button" data-assistant-query="${escapeHtml(query)}">${escapeHtml(label)}</button>`).join("")}
    </div>
  `;
}

function isActionableAssistantQuery(query) {
  const value = String(query || "").trim();
  if (!value) return false;
  const lowered = value.toLowerCase();
  const placeholderHints = [
    "another suspect",
    "a named person",
    "named person",
    "specific fir",
    "specific case",
    "this case",
    "this crime type",
    "same mo",
    "same case",
    "{subject}",
  ];
  return !placeholderHints.some((hint) => lowered.includes(hint));
}

function parseAssistantSections(content) {
  const sections = {};
  String(content ?? "")
    .split(/\n{2,}/)
    .forEach((block) => {
      const match = block.match(/^([A-Za-z][A-Za-z -]+):\n([\s\S]*)$/);
      if (match) sections[match[1].trim()] = match[2].trim();
    });
  return sections;
}

function renderAssistantEvidence(intelligence) {
  if (intelligence?.presentation?.render_evidence === false) return "";
  const sources = Array.isArray(intelligence.sources) ? intelligence.sources : [];
  const safeguards = Array.isArray(intelligence.safeguards) ? intelligence.safeguards : [];
  const sourceBlock = sources.length ? renderSourceCards(sources) : renderAggregateSourceNote(intelligence);
  const evidenceCount = sources.length || Number(intelligence.visible_case_count || 0) || 0;
  const showConfidence = intelligence?.presentation?.show_confidence === true && intelligence.confidence;
  return `
    <div class="assistant-meta">
      <details class="assistant-evidence">
        <summary>
          <span><i data-lucide="list-search"></i>Evidence Sources (${escapeHtml(formatCount(evidenceCount))})</span>
          <i data-lucide="chevron-down"></i>
        </summary>
        <div class="assistant-evidence-body">
          <div class="evidence-chips">
            ${evidenceChip(t("recordsMatched"), formatCount(intelligence.visible_case_count))}
            ${evidenceChip(t("sourceRecords"), String(sources.length))}
            ${showConfidence ? evidenceChip("Confidence", shorten(intelligence.confidence, 64)) : ""}
          </div>
          ${sourceBlock}
          ${renderSafeguards(safeguards)}
        </div>
      </details>
    </div>
  `;
}

function formatAnswerSupportLine(intelligence, sourceCount) {
  const recordCount = Number(intelligence.visible_case_count || 0);
  const recordText = recordCount === 1 ? t("oneRecordFound") : `${formatCount(recordCount)} ${t("recordsFound")}`;
  if (!sourceCount) return recordText;
  const sourceText = sourceCount === 1 ? t("oneSourceRecord") : `${sourceCount} ${t("sourceRecordsLower")}`;
  return `${recordText} • ${sourceText}`;
}

function renderOrchestrationTrace(trace) {
  if (!Array.isArray(trace) || !trace.length) return "";
  return `
    <section class="query-analysis">
      <h3>${escapeHtml(t("orchestrationFlow"))}</h3>
      <div class="query-analysis-grid">
        ${trace.map((stage, index) => analysisRow(String(index + 1), stage)).join("")}
      </div>
    </section>
  `;
}

function evidenceChip(label, value) {
  return `<span class="evidence-chip"><span>${escapeHtml(label)}</span><b>${escapeHtml(value)}</b></span>`;
}

function labelEvidenceMode(value) {
  const mode = String(value || "crime_data_only");
  const map = {
    imported_incident_aggregate: "importedAggregate",
    local_case_search_index: "localSearchIndex",
    local_case_records: "sourceRecords",
  };
  return t(map[mode] || mode, mode.replaceAll("_", " "));
}

function renderQueryAnalysis(analysis) {
  if (!analysis || !Object.keys(analysis).length) return "";
  const terms = Array.isArray(analysis.interpreted_terms) ? analysis.interpreted_terms : [];
  const filters = analysis.interpreted_filters || {};
  return `
    <section class="query-analysis">
      <h3>${escapeHtml(t("queryInterpretation"))}</h3>
      <div class="query-analysis-grid">
        ${analysis.normalized_query ? analysisRow(t("normalized"), analysis.normalized_query) : ""}
        ${terms.length ? analysisRow(t("terms"), terms.join(", ")) : ""}
        ${Object.keys(filters).length ? analysisRow(t("filters"), formatFilters(filters)) : ""}
      </div>
    </section>
  `;
}

function analysisRow(label, value) {
  return `<span><b>${escapeHtml(label)}</b>${escapeHtml(value)}</span>`;
}

function formatFilters(filters) {
  return Object.entries(filters)
    .map(([key, value]) => {
      const rendered = Array.isArray(value) ? value.join(", ") : String(value);
      return `${labelValue(key)}: ${rendered}`;
    })
    .join(" / ");
}

function renderSourceCards(sources) {
  return `
    <section class="source-list">
      <h3>${escapeHtml(t("evidenceSources"))} (${sources.length})</h3>
      <div class="source-grid">
        ${sources
          .slice(0, 5)
          .map((source) => `
            <article class="source-card">
              <header>
                <strong>${escapeHtml(source.fir_number || source.case_id || t("unknown"))}</strong>
                ${source.status ? statusBadge(source.status) : ""}
              </header>
              <p>${escapeHtml([source.district, source.sensitivity].filter(Boolean).join(" / "))}</p>
              ${source.excerpt ? `<p>${escapeHtml(shorten(source.excerpt, 210))}</p>` : ""}
            </article>
          `)
          .join("")}
      </div>
    </section>
  `;
}

function renderAggregateSourceNote(intelligence) {
  if (!Number(intelligence.visible_case_count || 0)) return "";
  return `<div class="aggregate-note"><i data-lucide="database"></i><span>${escapeHtml(t("noIndividualSources"))}</span></div>`;
}

function renderSafeguards(safeguards) {
  if (!safeguards.length) return "";
  return `
    <div class="safeguard-list" aria-label="${escapeHtml(t("safeguards"))}">
      ${safeguards.slice(0, 3).map((item) => `<span><i data-lucide="shield-check"></i>${escapeHtml(item)}</span>`).join("")}
    </div>
  `;
}

function formatCount(value) {
  return Number(value || 0).toLocaleString("en-IN");
}

async function handleTranslate() {
  const [source_language, target_language] = state.translationMode.split("-");
  try {
    const data = await api("/translate", {
      method: "POST",
      body: JSON.stringify({
        text: $("#translateInput").value,
        source_language,
        target_language,
      }),
    });
    $("#translationResult").innerHTML = `<strong>${escapeHtml(data.translated_text)}</strong><p>${escapeHtml(data.provider)} / confidence ${Math.round(data.confidence * 100)}%</p>`;
  } catch (error) {
    renderPermission("#translationResult", error.message);
  }
}

async function exportPdf() {
  if (!state.conversationId) {
    await createConversation();
  }
  try {
    const response = await fetch(`/conversations/${state.conversationId}/export.pdf`, {
      headers: { Authorization: `Bearer ${state.token}` },
    });
    if (!response.ok) throw new Error("PDF export failed");
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${state.conversationId}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    renderPermission("#translationResult", error.message);
  }
}

async function loadProfile() {
  const suspect = $("#suspectInput").value.trim();
  if (!suspect) return;
  try {
    const profile = await api(`/profiles/suspects/${encodeURIComponent(suspect)}`);
    $("#profileResult").innerHTML = `
      <strong>${escapeHtml(profile.suspect_name)}</strong>
      <p>${escapeHtml(profile.profile)}</p>
      <p>${escapeHtml(t("districts"))}: ${escapeHtml(profile.districts.join(", ") || t("none"))}</p>
      <p>${escapeHtml(t("riskScore"))}: ${escapeHtml(String(profile.risk_score))} / ${escapeHtml(labelValue(profile.risk_level))}</p>
      <ul>${profile.behavioral_indicators.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    `;
  } catch (error) {
    renderPermission("#profileResult", error.message);
  }
}

async function loadSupport() {
  const caseId = $("#caseSelect").value;
  if (!caseId) return;
  try {
    const support = await api(`/decision-support/cases/${caseId}`);
    $("#supportResult").innerHTML = `
      <strong>${escapeHtml(support.summary)}</strong>
      <h3>${escapeHtml(t("investigationTimeline"))}</h3>
      <ul>${support.investigation_timeline.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <h3>${escapeHtml(t("nextSteps"))}</h3>
      <ul>${support.recommended_next_steps.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <h3>${escapeHtml(t("investigativeLeads"))}</h3>
      <ul>${support.investigative_leads.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <h3>${escapeHtml(t("similarCases"))}</h3>
      <ul>${support.similar_cases.map((item) => `<li>${escapeHtml(item.fir_number)}: ${escapeHtml(item.reason)}</li>`).join("") || "<li>No similar accessible cases.</li>"}</ul>
    `;
  } catch (error) {
    renderPermission("#supportResult", error.message);
  }
}

async function loadExplanation() {
  const caseId = $("#caseSelect").value;
  if (!caseId) return;
  try {
    const explanation = await api(`/explain/cases/${caseId}`);
    $("#explainResult").innerHTML = `
      <strong>${escapeHtml(explanation.explanation)}</strong>
      <ul>${explanation.factors.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <h3>${escapeHtml(t("reasoningPath"))}</h3>
      <ol>${explanation.reasoning_path.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ol>
      <h3>${escapeHtml(t("correlations"))}</h3>
      <ul>${explanation.correlations.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <p>${escapeHtml(t("evidenceHash"))}: ${escapeHtml(explanation.audit.evidence_hash || t("unavailable"))}</p>
    `;
  } catch (error) {
    renderPermission("#explainResult", error.message);
  }
}

function renderAudit(integrity, logs) {
  $("#auditIntegrity").innerHTML = `
    <strong>${integrity.valid ? escapeHtml(t("chainValid")) : escapeHtml(t("chainFailed"))}</strong>
    <p>${escapeHtml(t("checkedAuditEvents"))}: ${integrity.checked}</p>
  `;
  $("#auditLogs").innerHTML = logs
    .map((item) => listItem(item.action, `${item.status} / ${item.resource_type} / ${formatDate(item.created_at)}`))
    .join("");
}

function renderPermission(selector, message) {
  const node = $(selector);
  if (!node) return;
  node.innerHTML = listItem(t("unavailable"), message || t("roleCannotAccess"));
}

function metric(label, value, caption) {
  return `<article class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong><span>${escapeHtml(caption)}</span></article>`;
}

function topChip(label, value) {
  return `<span class="top-chip"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></span>`;
}

function listItem(title, body, className = "") {
  return `
    <article class="list-item ${className}">
      <header><strong>${escapeHtml(title)}</strong></header>
      <p>${escapeHtml(body)}</p>
    </article>
  `;
}

function barRows(group, buckets) {
  const max = Math.max(1, ...buckets.map((item) => item.count));
  return buckets.map((item) => {
    const width = Math.max(5, Math.round((item.count / max) * 100));
    return `
      <div class="bar-row">
        <header><span>${escapeHtml(group)} / ${escapeHtml(item.key)}</span><strong>${item.count}</strong></header>
        <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
      </div>
    `;
  });
}

function statusBadge(value) {
  return `<span class="badge">${escapeHtml(labelValue(value))}</span>`;
}

function formatMoney(value) {
  return Number(value || 0).toLocaleString("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  });
}

function prettyBytes(value) {
  const bytes = Number(value || 0);
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let size = bytes / 1024;
  let unitIndex = 0;
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex += 1;
  }
  return `${size.toFixed(size >= 10 ? 0 : 1)} ${units[unitIndex]}`;
}

function formatDate(value) {
  return new Date(value).toLocaleString(state.language === "kn" ? "kn-IN" : undefined);
}

function shorten(value, max) {
  const text = String(value);
  return text.length > max ? `${text.slice(0, max - 1)}.` : text;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll(" ", "-");
}

function cssEscape(value) {
  if (window.CSS?.escape) return CSS.escape(value);
  return String(value).replaceAll("\\", "\\\\").replaceAll('"', '\\"');
}

function labelValue(value) {
  const key = String(value ?? "").replaceAll("-", "_").replaceAll(" ", "_").toLowerCase();
  const map = {
    active: "active",
    analyst: "analyst",
    closed: "closed",
    high: "high",
    high_value_transfer: "highValueTransfer",
    bank: "bank",
    bank_manager: "bankManager",
    branch: "branch",
    dead_end: "deadEnd",
    financial_account: "financialAccount",
    ifsc: "ifsc",
    investigator: "investigator",
    policymaker: "policymaker",
    low: "low",
    medium: "medium",
    open: "open",
    possible_circular_flow: "possibleCircularFlow",
    possible_structuring: "possibleStructuring",
    restricted: "restricted",
    standard: "standard",
    super_admin: "superAdmin",
    supervisor: "supervisor",
    under_review: "underReview",
    viewer: "viewer",
    victim_age: "victimAge",
    victim_gender: "victimGender",
    suspect_age: "suspectAge",
    suspect_gender: "suspectGender",
  };
  return t(map[key] || key, String(value ?? "").replaceAll("_", " "));
}

function moduleLabel(module) {
  const map = {
    chat_interface: "moduleChat",
    decision_support: "moduleDecision",
    explainable_ai: "moduleExplain",
    financial_analysis: "moduleFinancial",
    forecasting: "moduleForecast",
    geospatial_mapping: "moduleGeo",
    hash_prefix_search: "moduleSearch",
    advanced_crime_ml: "moduleAdvanced",
    network_analysis: "moduleNetwork",
    offender_profiling: "moduleProfile",
    pattern_discovery: "modulePatterns",
    rbac: "moduleGovernance",
    sociological_insights: "moduleSocio",
    super_admin: "moduleAdmin",
    translation_voice_pdf: "moduleLanguage",
    trend_analytics: "moduleTrends",
  };
  return t(map[module.id] || module.id, module.name);
}

function moduleStatusLabel(status) {
  if (state.language === "en") return status;
  if (status.includes("implemented")) return t("implemented");
  return status;
}

function debounce(fn, wait) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), wait);
  };
}

document.addEventListener("DOMContentLoaded", boot);
