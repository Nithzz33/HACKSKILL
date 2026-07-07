from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go


ROLE_COLORS = {
    "High-risk Suspect": "#e53935",
    "Gang Leader": "#fb8c00",
    "Associate": "#1e88e5",
    "Financial Facilitator": "#2e7d32",
    "Facilitator": "#43a047",
    "Communication Broker": "#7b1fa2",
}

COMMUNITY_COLORS = [
    "#b71c1c",
    "#004d40",
    "#0d47a1",
    "#4a148c",
    "#e65100",
    "#1b5e20",
    "#263238",
    "#880e4f",
    "#3e2723",
    "#827717",
]

RELATIONSHIP_DASH = {
    "Phone Call": "dash",
    "Money Transfer": "dot",
    "Meeting": "solid",
    "Social Relationship": "longdash",
}


@dataclass(frozen=True)
class DashboardConfig:
    node_count: int = 100
    edge_count: int = 250
    seed: int = 20260609
    start_date: date = date(2025, 1, 1)
    end_date: date = date(2026, 6, 9)
    output_dir: Path = Path("outputs/criminal_network")


def build_name_pool() -> list[str]:
    first_names = [
        "Ravi",
        "Kiran",
        "Arjun",
        "Naveen",
        "Prakash",
        "Manjunath",
        "Sanjay",
        "Karthik",
        "Sameer",
        "Vikram",
        "Rahul",
        "Deepak",
        "Ramesh",
        "Anil",
        "Imran",
        "Yusuf",
        "Farhan",
        "Mohan",
        "Dinesh",
        "Harish",
        "Meera",
        "Asha",
        "Nandini",
        "Sahana",
        "Lakshmi",
        "Priya",
        "Kavya",
        "Reshma",
        "Zoya",
        "Pooja",
    ]
    last_names = [
        "Kumar",
        "Shetty",
        "Gowda",
        "Rao",
        "Patil",
        "Naik",
        "Khan",
        "Ahmed",
        "Hegde",
        "Iyer",
        "Reddy",
        "Nayak",
        "Pasha",
        "Murthy",
        "Nair",
        "Das",
        "Singh",
        "Ali",
        "Bhat",
        "Kulkarni",
    ]
    names: list[str] = []
    for first in first_names:
        for last in last_names:
            names.append(f"{first} {last}")
    return names


def random_date(rng: random.Random, start: date, end: date) -> str:
    days = (end - start).days
    return (start + timedelta(days=rng.randint(0, days))).isoformat()


def make_synthetic_nodes(config: DashboardConfig) -> pd.DataFrame:
    rng = random.Random(config.seed)
    names = build_name_pool()
    rng.shuffle(names)

    role_plan = (
        ["Gang Leader"] * 6
        + ["High-risk Suspect"] * 18
        + ["Communication Broker"] * 12
        + ["Financial Facilitator"] * 16
        + ["Facilitator"] * 10
        + ["Associate"] * 38
    )
    if len(role_plan) != config.node_count:
        raise ValueError("Role plan must match node_count")
    rng.shuffle(role_plan)

    districts = [
        ("Bengaluru", 12.9716, 77.5946),
        ("Mysuru", 12.2958, 76.6394),
        ("Mangaluru", 12.9141, 74.8560),
        ("Belagavi", 15.8497, 74.4977),
        ("Hubballi-Dharwad", 15.3647, 75.1240),
        ("Kalaburagi", 17.3297, 76.8343),
        ("Ballari", 15.1394, 76.9214),
        ("Shivamogga", 13.9299, 75.5681),
        ("Tumakuru", 13.3379, 77.1173),
        ("Udupi", 13.3409, 74.7421),
    ]
    alias_words = ["Falcon", "Ledger", "Wire", "Pilot", "Shadow", "Relay", "North", "Tiger", "Cipher", "Anchor"]
    rows: list[dict[str, Any]] = []
    for index in range(config.node_count):
        role = role_plan[index]
        base_risk = {
            "Gang Leader": (82, 98),
            "High-risk Suspect": (70, 95),
            "Communication Broker": (55, 88),
            "Financial Facilitator": (58, 92),
            "Facilitator": (45, 80),
            "Associate": (25, 72),
        }[role]
        district, lat, lon = rng.choice(districts)
        seed_cell = index % 7
        rows.append(
            {
                "person_id": f"SUS-{index + 1:04d}",
                "name": names[index],
                "alias": f"{rng.choice(alias_words)}-{rng.randint(10, 99)}",
                "role": role,
                "risk_score": rng.randint(*base_risk),
                "seed_cell": seed_cell,
                "district": district,
                "latitude": round(lat + rng.uniform(-0.18, 0.18), 6),
                "longitude": round(lon + rng.uniform(-0.18, 0.18), 6),
                "first_seen": random_date(rng, date(2023, 1, 1), config.end_date),
            }
        )
    return pd.DataFrame(rows)


def make_edge(
    edge_id: int,
    source: str,
    target: str,
    relationship_type: str,
    weight: int,
    occurred_on: str,
    rng: random.Random,
    money_chain_id: str | None = None,
) -> dict[str, Any]:
    amount = 0.0
    channel = rng.choice(["Direct", "Encrypted App", "Cash Courier", "Bank Transfer", "Shell Entity"])
    if relationship_type == "Money Transfer":
        amount = float(rng.randint(80_000, 4_800_000))
        channel = rng.choice(["UPI mule", "IMPS", "RTGS", "Cash deposit", "Shell account"])
    return {
        "edge_id": f"REL-{edge_id:04d}",
        "source": source,
        "target": target,
        "relationship_type": relationship_type,
        "weight": int(weight),
        "occurred_on": occurred_on,
        "amount_inr": amount,
        "channel": channel,
        "money_chain_id": money_chain_id or "",
    }


def add_unique_edge(
    rows: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    edge_id: int,
    source: str,
    target: str,
    relationship_type: str,
    weight: int,
    occurred_on: str,
    rng: random.Random,
    money_chain_id: str | None = None,
) -> int:
    if source == target:
        return edge_id
    key = (source, target, relationship_type)
    if key in seen:
        return edge_id
    seen.add(key)
    rows.append(make_edge(edge_id, source, target, relationship_type, weight, occurred_on, rng, money_chain_id))
    return edge_id + 1


def make_synthetic_edges(nodes: pd.DataFrame, config: DashboardConfig) -> pd.DataFrame:
    rng = random.Random(config.seed + 17)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    edge_id = 1

    by_cell = {
        int(cell): group["person_id"].tolist()
        for cell, group in nodes.groupby("seed_cell", sort=True)
    }
    leaders = nodes[nodes["role"] == "Gang Leader"]["person_id"].tolist()
    brokers = nodes[nodes["role"] == "Communication Broker"]["person_id"].tolist()
    finance_nodes = nodes[nodes["role"].isin(["Financial Facilitator", "Facilitator"])]["person_id"].tolist()
    high_risk = nodes[nodes["role"].isin(["High-risk Suspect", "Gang Leader"])]["person_id"].tolist()
    all_ids = nodes["person_id"].tolist()

    # Strong intra-cell leadership and meetings create realistic clusters.
    for cell, members in by_cell.items():
        leader = leaders[cell % len(leaders)]
        if leader not in members:
            members = [leader, *members]
        for member in members[:13]:
            if member == leader:
                continue
            edge_id = add_unique_edge(
                rows,
                seen,
                edge_id,
                leader,
                member,
                rng.choice(["Meeting", "Phone Call", "Social Relationship"]),
                rng.randint(5, 10),
                random_date(rng, config.start_date, config.end_date),
                rng,
            )

    # Communication brokers deliberately bridge cells.
    for broker in brokers:
        targets = rng.sample([node for node in all_ids if node != broker], 5)
        for target in targets:
            edge_id = add_unique_edge(
                rows,
                seen,
                edge_id,
                broker,
                target,
                "Phone Call",
                rng.randint(4, 10),
                random_date(rng, config.start_date, config.end_date),
                rng,
            )

    # Money laundering chains are encoded explicitly for highlighting and Sankey analysis.
    chain_roots = rng.sample(high_risk, 5)
    chain_targets = rng.sample(finance_nodes, 25)
    for chain_index, root in enumerate(chain_roots, start=1):
        chain = [root, *chain_targets[(chain_index - 1) * 5 : chain_index * 5]]
        for step, (source, target) in enumerate(zip(chain, chain[1:]), start=1):
            edge_id = add_unique_edge(
                rows,
                seen,
                edge_id,
                source,
                target,
                "Money Transfer",
                rng.randint(6, 10),
                random_date(rng, config.start_date, config.end_date),
                rng,
                money_chain_id=f"ML-{chain_index:02d}",
            )

    relationship_types = ["Phone Call", "Money Transfer", "Meeting", "Social Relationship"]
    while len(rows) < config.edge_count:
        if rng.random() < 0.72:
            cell = rng.choice(list(by_cell))
            source, target = rng.sample(by_cell[cell], 2)
        else:
            source, target = rng.sample(all_ids, 2)
        relationship_type = rng.choices(relationship_types, weights=[0.36, 0.22, 0.22, 0.20], k=1)[0]
        edge_id = add_unique_edge(
            rows,
            seen,
            edge_id,
            source,
            target,
            relationship_type,
            rng.randint(1, 10),
            random_date(rng, config.start_date, config.end_date),
            rng,
        )

    return pd.DataFrame(rows[: config.edge_count])


def build_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> tuple[nx.DiGraph, nx.Graph]:
    directed = nx.DiGraph()
    for row in nodes.to_dict("records"):
        directed.add_node(row["person_id"], **row)
    for row in edges.to_dict("records"):
        source = row["source"]
        target = row["target"]
        weight = float(row["weight"])
        if directed.has_edge(source, target):
            directed[source][target]["weight"] += weight
            directed[source][target]["relationship_count"] += 1
        else:
            directed.add_edge(source, target, weight=weight, relationship_count=1)

    undirected = nx.Graph()
    for row in nodes.to_dict("records"):
        undirected.add_node(row["person_id"], **row)
    for row in edges.to_dict("records"):
        source = row["source"]
        target = row["target"]
        weight = float(row["weight"])
        if undirected.has_edge(source, target):
            undirected[source][target]["weight"] += weight
        else:
            undirected.add_edge(source, target, weight=weight)
    for source, target, data in undirected.edges(data=True):
        data["distance"] = 1.0 / max(float(data["weight"]), 1.0)
    return directed, undirected


def detect_communities(graph: nx.Graph, seed: int) -> dict[str, int]:
    try:
        communities = nx.community.louvain_communities(graph, weight="weight", seed=seed)
    except Exception:
        communities = list(nx.community.greedy_modularity_communities(graph, weight="weight"))
    sorted_communities = sorted(communities, key=lambda members: (-len(members), sorted(members)[0]))
    assignments: dict[str, int] = {}
    for community_id, members in enumerate(sorted_communities):
        for node_id in members:
            assignments[str(node_id)] = community_id
    return assignments


def weighted_pagerank(graph: nx.DiGraph, damping: float = 0.85, max_iter: int = 200, tolerance: float = 1.0e-9) -> dict[str, float]:
    """Compute weighted PageRank without requiring SciPy at runtime."""
    node_ids = list(graph.nodes)
    if not node_ids:
        return {}
    node_count = len(node_ids)
    rank = {node_id: 1.0 / node_count for node_id in node_ids}
    out_weight = {
        node_id: sum(float(graph[node_id][target].get("weight", 1.0)) for target in graph.successors(node_id))
        for node_id in node_ids
    }
    teleport = (1.0 - damping) / node_count
    for _ in range(max_iter):
        next_rank = {node_id: teleport for node_id in node_ids}
        sink_rank = sum(rank[node_id] for node_id in node_ids if out_weight[node_id] == 0)
        sink_share = damping * sink_rank / node_count
        for node_id in node_ids:
            next_rank[node_id] += sink_share
        for source in node_ids:
            if out_weight[source] == 0:
                continue
            for target in graph.successors(source):
                weight = float(graph[source][target].get("weight", 1.0))
                next_rank[target] += damping * rank[source] * (weight / out_weight[source])
        delta = sum(abs(next_rank[node_id] - rank[node_id]) for node_id in node_ids)
        rank = next_rank
        if delta < tolerance:
            break
    total = sum(rank.values()) or 1.0
    return {node_id: value / total for node_id, value in rank.items()}


def scale_series(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0)
    value_range = numeric.max() - numeric.min()
    if value_range == 0:
        return pd.Series(np.zeros(len(numeric)), index=numeric.index)
    return (numeric - numeric.min()) / value_range


def enrich_network(nodes: pd.DataFrame, edges: pd.DataFrame, config: DashboardConfig) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    directed, undirected = build_graph(nodes, edges)
    degree = nx.degree_centrality(undirected)
    betweenness = nx.betweenness_centrality(undirected, weight="distance", normalized=True)
    closeness = nx.closeness_centrality(undirected, distance="distance")
    try:
        eigenvector = nx.eigenvector_centrality(undirected, max_iter=1500, weight="weight")
    except nx.NetworkXException:
        eigenvector = {node_id: 0.0 for node_id in undirected.nodes}
    pagerank = weighted_pagerank(directed)
    communities = detect_communities(undirected, config.seed)

    edge_lookup = edges.copy()
    edge_lookup["is_money"] = edge_lookup["relationship_type"].eq("Money Transfer")
    communication_counts = (
        pd.concat(
            [
                edge_lookup[edge_lookup["relationship_type"].eq("Phone Call")]["source"],
                edge_lookup[edge_lookup["relationship_type"].eq("Phone Call")]["target"],
            ],
            ignore_index=True,
        )
        .value_counts()
        .to_dict()
    )
    transaction_counts = (
        pd.concat([edge_lookup[edge_lookup["is_money"]]["source"], edge_lookup[edge_lookup["is_money"]]["target"]], ignore_index=True)
        .value_counts()
        .to_dict()
    )
    money_totals = (
        pd.concat(
            [
                edge_lookup[edge_lookup["is_money"]][["source", "amount_inr"]].rename(columns={"source": "person_id"}),
                edge_lookup[edge_lookup["is_money"]][["target", "amount_inr"]].rename(columns={"target": "person_id"}),
            ],
            ignore_index=True,
        )
        .groupby("person_id")["amount_inr"]
        .sum()
        .to_dict()
    )

    enriched = nodes.copy()
    enriched["degree_centrality"] = enriched["person_id"].map(degree).fillna(0.0)
    enriched["betweenness_centrality"] = enriched["person_id"].map(betweenness).fillna(0.0)
    enriched["closeness_centrality"] = enriched["person_id"].map(closeness).fillna(0.0)
    enriched["eigenvector_centrality"] = enriched["person_id"].map(eigenvector).fillna(0.0)
    enriched["pagerank"] = enriched["person_id"].map(pagerank).fillna(0.0)
    enriched["community"] = enriched["person_id"].map(communities).fillna(-1).astype(int)
    enriched["known_associates"] = enriched["person_id"].map(lambda node_id: len(list(undirected.neighbors(node_id)))).astype(int)
    enriched["number_of_communications"] = enriched["person_id"].map(communication_counts).fillna(0).astype(int)
    enriched["number_of_transactions"] = enriched["person_id"].map(transaction_counts).fillna(0).astype(int)
    enriched["money_total_inr"] = enriched["person_id"].map(money_totals).fillna(0.0)

    community_sizes = enriched["community"].value_counts().to_dict()
    enriched["community_size"] = enriched["community"].map(community_sizes).fillna(0).astype(int)

    external_counts: dict[str, int] = {node_id: 0 for node_id in enriched["person_id"]}
    community_external_edges: dict[int, int] = {int(community): 0 for community in enriched["community"].unique()}
    for row in edges.to_dict("records"):
        source_community = int(enriched.loc[enriched["person_id"].eq(row["source"]), "community"].iloc[0])
        target_community = int(enriched.loc[enriched["person_id"].eq(row["target"]), "community"].iloc[0])
        if source_community != target_community:
            external_counts[row["source"]] += 1
            external_counts[row["target"]] += 1
            community_external_edges[source_community] = community_external_edges.get(source_community, 0) + 1
            community_external_edges[target_community] = community_external_edges.get(target_community, 0) + 1
    enriched["external_connections"] = enriched["person_id"].map(external_counts).fillna(0).astype(int)

    top_pagerank = set(enriched.nlargest(8, "pagerank")["person_id"])
    top_brokers = set(enriched.nlargest(8, "betweenness_centrality")["person_id"])
    money_chain_nodes = set(edges.loc[edges["money_chain_id"].ne(""), "source"]) | set(edges.loc[edges["money_chain_id"].ne(""), "target"])
    min_external_community = min(community_external_edges, key=community_external_edges.get)

    enriched["is_key_influencer"] = enriched["person_id"].isin(top_pagerank)
    enriched["is_bridge_node"] = enriched["person_id"].isin(top_brokers)
    enriched["is_money_laundering_chain"] = enriched["person_id"].isin(money_chain_nodes)
    enriched["is_isolated_cell"] = enriched["community"].eq(min_external_community)
    enriched["risk_level"] = pd.cut(
        enriched["risk_score"],
        bins=[-1, 44, 74, 100],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    enriched["anomaly_score"] = (
        0.25 * scale_series(enriched["risk_score"])
        + 0.20 * scale_series(enriched["degree_centrality"])
        + 0.20 * scale_series(enriched["betweenness_centrality"])
        + 0.15 * scale_series(enriched["number_of_transactions"])
        + 0.10 * scale_series(enriched["money_total_inr"])
        + 0.10 * scale_series(enriched["external_connections"])
    )
    enriched["anomaly_score"] = (100 * enriched["anomaly_score"]).round(2)

    for column in ["degree_centrality", "betweenness_centrality", "closeness_centrality", "eigenvector_centrality", "pagerank"]:
        enriched[column] = enriched[column].round(5)

    edges = edges.copy()
    source_community = enriched.set_index("person_id")["community"].to_dict()
    edges["source_community"] = edges["source"].map(source_community).astype(int)
    edges["target_community"] = edges["target"].map(source_community).astype(int)
    edges["is_cross_community"] = edges["source_community"].ne(edges["target_community"])

    components = list(nx.connected_components(undirected))
    largest = undirected.subgraph(max(components, key=len)).copy()
    metrics = {
        "density": round(nx.density(undirected), 4),
        "diameter": int(nx.diameter(largest)) if largest.number_of_nodes() > 1 else 0,
        "average_path_length": round(nx.average_shortest_path_length(largest), 4) if largest.number_of_nodes() > 1 else 0.0,
        "number_of_communities": int(enriched["community"].nunique()),
        "total_connections": int(len(edges)),
        "total_nodes": int(len(enriched)),
        "key_influencers": enriched.loc[enriched["is_key_influencer"], ["person_id", "name", "pagerank"]].to_dict("records"),
        "bridge_nodes": enriched.loc[enriched["is_bridge_node"], ["person_id", "name", "betweenness_centrality"]].to_dict("records"),
        "isolated_cell": int(min_external_community),
    }
    return enriched, edges, metrics


def compute_layout(nodes: pd.DataFrame, edges: pd.DataFrame, seed: int) -> dict[str, dict[str, float]]:
    _, undirected = build_graph(nodes, edges)
    raw_positions = nx.spring_layout(undirected, seed=seed, weight="weight", k=0.42, iterations=350)
    return {node_id: {"x": float(xy[0]), "y": float(xy[1])} for node_id, xy in raw_positions.items()}


def node_hover(row: pd.Series) -> str:
    return (
        f"<b>{row['name']}</b><br>"
        f"ID: {row['person_id']}<br>"
        f"Role: {row['role']}<br>"
        f"Community: {row['community']}<br>"
        f"Risk: {row['risk_score']} ({row['risk_level']})<br>"
        f"Degree: {row['degree_centrality']:.3f}<br>"
        f"Betweenness: {row['betweenness_centrality']:.3f}<br>"
        f"Closeness: {row['closeness_centrality']:.3f}<br>"
        f"Eigenvector: {row['eigenvector_centrality']:.3f}<br>"
        f"PageRank: {row['pagerank']:.3f}<br>"
        f"Anomaly: {row['anomaly_score']:.1f}"
    )


def create_network_figure(nodes: pd.DataFrame, edges: pd.DataFrame, positions: dict[str, dict[str, float]]) -> go.Figure:
    traces: list[go.Scatter] = []
    for row in edges.to_dict("records"):
        source = positions[row["source"]]
        target = positions[row["target"]]
        width = 0.65 + (float(row["weight"]) * 0.38)
        color = "rgba(0,0,0,0.50)"
        if row["money_chain_id"]:
            color = "rgba(18,115,55,0.72)"
            width += 1.2
        traces.append(
            go.Scatter(
                x=[source["x"], target["x"], None],
                y=[source["y"], target["y"], None],
                mode="lines",
                line={
                    "width": width,
                    "color": color,
                    "dash": RELATIONSHIP_DASH.get(row["relationship_type"], "solid"),
                },
                hoverinfo="text",
                text=(
                    f"{row['relationship_type']}<br>"
                    f"{row['source']} -> {row['target']}<br>"
                    f"Weight: {row['weight']}<br>Date: {row['occurred_on']}<br>"
                    f"Amount INR: {row['amount_inr']:,.0f}"
                ),
                showlegend=False,
            )
        )

    for community, group in nodes.groupby("community"):
        traces.append(
            go.Scatter(
                x=[positions[node_id]["x"] for node_id in group["person_id"]],
                y=[positions[node_id]["y"] for node_id in group["person_id"]],
                mode="markers",
                marker={
                    "size": 22 + (group["degree_centrality"] * 58),
                    "color": COMMUNITY_COLORS[int(community) % len(COMMUNITY_COLORS)],
                    "opacity": 0.18,
                    "line": {"width": 0},
                },
                hoverinfo="skip",
                showlegend=False,
            )
        )

    for role, group in nodes.groupby("role"):
        traces.append(
            go.Scatter(
                x=[positions[node_id]["x"] for node_id in group["person_id"]],
                y=[positions[node_id]["y"] for node_id in group["person_id"]],
                mode="markers+text",
                name=role,
                text=group["name"].tolist(),
                textposition="top center",
                textfont={"size": 8, "color": "#111"},
                marker={
                    "size": 12 + (group["degree_centrality"] * 68),
                    "color": ROLE_COLORS.get(role, "#546e7a"),
                    "opacity": 0.95,
                    "line": {
                        "width": np.where(group["is_bridge_node"] | group["is_key_influencer"], 4, 2),
                        "color": [COMMUNITY_COLORS[int(value) % len(COMMUNITY_COLORS)] for value in group["community"]],
                    },
                },
                customdata=group["person_id"].tolist(),
                hovertext=[node_hover(row) for _, row in group.iterrows()],
                hoverinfo="text",
            )
        )

    figure = go.Figure(data=traces)
    figure.update_layout(
        title={
            "text": "Criminal Network Analysis - Synthetic Intelligence Graph",
            "x": 0.02,
            "xanchor": "left",
            "font": {"color": "#9b111e", "size": 22},
        },
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True,
        legend={
            "x": 0.01,
            "y": 0.98,
            "bgcolor": "rgba(255,255,255,0.86)",
            "bordercolor": "#d8d8d8",
            "borderwidth": 1,
        },
        margin={"l": 12, "r": 12, "t": 64, "b": 12},
        xaxis={"visible": False},
        yaxis={"visible": False},
        width=1600,
        height=980,
    )
    return figure


def create_sankey_figure(nodes: pd.DataFrame, edges: pd.DataFrame) -> go.Figure:
    money_edges = edges[edges["relationship_type"].eq("Money Transfer")].nlargest(48, "amount_inr")
    names = nodes.set_index("person_id")["name"].to_dict()
    labels = sorted(set(money_edges["source"]) | set(money_edges["target"]))
    index = {node_id: idx for idx, node_id in enumerate(labels)}
    figure = go.Figure(
        data=[
            go.Sankey(
                node={"label": [f"{names[node_id]}<br>{node_id}" for node_id in labels], "pad": 12, "thickness": 13},
                link={
                    "source": [index[row["source"]] for row in money_edges.to_dict("records")],
                    "target": [index[row["target"]] for row in money_edges.to_dict("records")],
                    "value": [max(row["amount_inr"] / 100000.0, 1.0) for row in money_edges.to_dict("records")],
                    "color": ["rgba(46,125,50,0.35)" for _ in range(len(money_edges))],
                },
            )
        ]
    )
    figure.update_layout(title="Sankey - Financial Transaction Flow", font={"size": 11}, paper_bgcolor="white")
    return figure


def create_temporal_figure(edges: pd.DataFrame) -> go.Figure:
    monthly = edges.copy()
    monthly["month"] = pd.to_datetime(monthly["occurred_on"]).dt.to_period("M").astype(str)
    pivot = monthly.pivot_table(index="month", columns="relationship_type", values="edge_id", aggfunc="count", fill_value=0)
    figure = go.Figure()
    for column in pivot.columns:
        figure.add_trace(go.Scatter(x=pivot.index, y=pivot[column], mode="lines+markers", name=column))
    figure.update_layout(
        title="Temporal Network Evolution",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Month",
        yaxis_title="Relationship events",
    )
    return figure


def create_heatmap_figure(nodes: pd.DataFrame) -> go.Figure:
    figure = go.Figure(
        go.Densitymapbox(
            lat=nodes["latitude"],
            lon=nodes["longitude"],
            z=nodes["risk_score"],
            radius=22,
            colorscale="YlOrRd",
            hoverinfo="text",
            text=[f"{row.name} / Risk {row.risk_score}" for row in nodes.itertuples(index=False)],
        )
    )
    figure.update_layout(
        title="Geographic Risk Heatmap - Karnataka",
        mapbox={"style": "carto-positron", "center": {"lat": 14.65, "lon": 75.65}, "zoom": 5.6},
        margin={"l": 0, "r": 0, "t": 42, "b": 0},
        paper_bgcolor="white",
        height=480,
    )
    return figure


def write_static_network_png(nodes: pd.DataFrame, edges: pd.DataFrame, positions: dict[str, dict[str, float]], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    line_styles = {
        "Phone Call": "--",
        "Money Transfer": ":",
        "Meeting": "-",
        "Social Relationship": "-.",
    }
    fig, ax = plt.subplots(figsize=(16, 9.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for row in edges.to_dict("records"):
        source = positions[row["source"]]
        target = positions[row["target"]]
        is_money_chain = bool(row["money_chain_id"])
        ax.plot(
            [source["x"], target["x"]],
            [source["y"], target["y"]],
            color="#127337" if is_money_chain else "#111111",
            alpha=0.62 if is_money_chain else 0.35,
            linewidth=0.35 + (float(row["weight"]) * 0.22) + (0.8 if is_money_chain else 0.0),
            linestyle=line_styles.get(row["relationship_type"], "-"),
            zorder=1,
        )

    for community, group in nodes.groupby("community"):
        ax.scatter(
            [positions[node_id]["x"] for node_id in group["person_id"]],
            [positions[node_id]["y"] for node_id in group["person_id"]],
            s=160 + (group["degree_centrality"] * 1300),
            c=COMMUNITY_COLORS[int(community) % len(COMMUNITY_COLORS)],
            alpha=0.12,
            edgecolors="none",
            zorder=2,
        )

    for role, group in nodes.groupby("role"):
        edge_colors = [COMMUNITY_COLORS[int(value) % len(COMMUNITY_COLORS)] for value in group["community"]]
        ax.scatter(
            [positions[node_id]["x"] for node_id in group["person_id"]],
            [positions[node_id]["y"] for node_id in group["person_id"]],
            s=48 + (group["degree_centrality"] * 1800),
            c=ROLE_COLORS.get(role, "#546e7a"),
            edgecolors=edge_colors,
            linewidths=np.where(group["is_bridge_node"] | group["is_key_influencer"], 1.7, 0.8),
            alpha=0.96,
            label=role,
            zorder=3,
        )
        for _, node in group.iterrows():
            x = positions[node["person_id"]]["x"]
            y = positions[node["person_id"]]["y"]
            ax.text(x + 0.006, y + 0.006, str(node["name"]), fontsize=3.9, color="#111111", zorder=4)

    legend_handles = [
        Line2D([0], [0], marker="o", color="w", label=role, markerfacecolor=color, markersize=8)
        for role, color in ROLE_COLORS.items()
    ]
    legend_handles.extend(
        [
            Line2D([0], [0], color="#111111", lw=1.4, linestyle=line_styles["Meeting"], label="Meeting"),
            Line2D([0], [0], color="#111111", lw=1.4, linestyle=line_styles["Phone Call"], label="Phone Call"),
            Line2D([0], [0], color="#111111", lw=1.4, linestyle=line_styles["Social Relationship"], label="Social Relationship"),
            Line2D([0], [0], color="#127337", lw=2.0, linestyle=line_styles["Money Transfer"], label="Money laundering chain"),
        ]
    )
    ax.legend(handles=legend_handles, loc="upper left", frameon=True, framealpha=0.92, fontsize=7)
    ax.set_title("Criminal Network Analysis - 100 Nodes / 250 Relationships", loc="left", color="#9b111e", fontsize=14, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=0.4)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def compute_link_predictions(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    _, graph = build_graph(nodes, edges)
    candidate_rows: list[dict[str, Any]] = []
    for source, target, score in nx.adamic_adar_index(graph):
        shared_neighbors = len(list(nx.common_neighbors(graph, source, target)))
        if shared_neighbors == 0:
            continue
        candidate_rows.append(
            {
                "source": source,
                "target": target,
                "prediction_score": round(float(score), 5),
                "shared_neighbors": shared_neighbors,
                "recommended_collection": "Validate phone CDR overlap and financial mule account reuse",
            }
        )
    predictions = pd.DataFrame(candidate_rows)
    if predictions.empty:
        return predictions
    return predictions.sort_values(["prediction_score", "shared_neighbors"], ascending=False).head(25)


def compute_shortest_paths(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    _, graph = build_graph(nodes, edges)
    leaders = nodes.nlargest(5, "pagerank")["person_id"].tolist()
    brokers = nodes.nlargest(5, "betweenness_centrality")["person_id"].tolist()
    rows: list[dict[str, Any]] = []
    for source in leaders:
        for target in brokers:
            if source == target:
                continue
            try:
                path = nx.shortest_path(graph, source=source, target=target, weight="distance")
                distance = nx.shortest_path_length(graph, source=source, target=target, weight="distance")
            except nx.NetworkXNoPath:
                continue
            rows.append(
                {
                    "source": source,
                    "target": target,
                    "hop_count": len(path) - 1,
                    "weighted_distance": round(float(distance), 4),
                    "path": " -> ".join(path),
                }
            )
    if not rows:
        return pd.DataFrame(columns=["source", "target", "hop_count", "weighted_distance", "path"])
    return pd.DataFrame(rows).sort_values(["hop_count", "weighted_distance"]).head(12)


def to_json_records(frame: pd.DataFrame) -> str:
    return json.dumps(frame.replace({np.nan: None}).to_dict("records"), ensure_ascii=False)


def render_dashboard_html(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    positions: dict[str, dict[str, float]],
    metrics: dict[str, Any],
    sankey: go.Figure,
    temporal: go.Figure,
    heatmap: go.Figure,
    link_predictions: pd.DataFrame,
    shortest_paths: pd.DataFrame,
) -> str:
    template = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Criminal Network Analysis Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {
      --red: #9b111e;
      --ink: #151515;
      --muted: #5f6368;
      --line: #d8d8d8;
      --soft: #f6f7f9;
      --panel: #ffffff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: #fff;
      font-family: Inter, Segoe UI, Arial, sans-serif;
    }
    .dashboard {
      display: grid;
      grid-template-columns: minmax(280px, 330px) minmax(0, 1fr);
      min-height: 100vh;
    }
    .profile {
      border-right: 1px solid var(--line);
      padding: 18px;
      background: linear-gradient(180deg, #fff 0%, #fafafa 100%);
    }
    .profile h1, .main h1 {
      margin: 0 0 14px;
      color: var(--red);
      font-size: 22px;
      letter-spacing: 0;
    }
    .search-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 42px;
      gap: 8px;
      margin-bottom: 14px;
    }
    input, select, button {
      height: 38px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #fff;
      padding: 0 10px;
      font: inherit;
    }
    button {
      cursor: pointer;
      background: var(--soft);
      font-weight: 650;
    }
    .photo {
      width: 100%;
      aspect-ratio: 1.15;
      display: grid;
      place-items: center;
      border: 1px solid #cfcfcf;
      background:
        linear-gradient(90deg, rgba(0,0,0,0.06) 1px, transparent 1px),
        linear-gradient(0deg, rgba(0,0,0,0.06) 1px, transparent 1px),
        #eceff1;
      background-size: 22px 22px;
      color: #424242;
      font-size: 46px;
      font-weight: 800;
      margin-bottom: 14px;
    }
    .identity h2 {
      margin: 0 0 4px;
      font-size: 19px;
      color: var(--red);
    }
    .identity p { margin: 0 0 12px; color: var(--muted); }
    .kv {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px 12px;
      padding: 12px 0;
      border-top: 1px solid var(--line);
    }
    .kv span:nth-child(odd) { font-weight: 700; }
    .score-row {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      margin: 8px 0;
      align-items: center;
    }
    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 8px;
      vertical-align: middle;
    }
    .badge-row {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 10px;
    }
    .badge {
      border: 1px solid #d0d0d0;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 12px;
      background: #fff;
    }
    .main {
      padding: 18px 20px 24px;
      overflow: hidden;
    }
    .toolbar {
      display: grid;
      grid-template-columns: repeat(5, minmax(140px, 1fr));
      gap: 10px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
      margin-bottom: 12px;
    }
    .toolbar label {
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    .relation-filter {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      grid-column: span 2;
    }
    .relation-filter label {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: var(--ink);
      font-size: 12px;
      font-weight: 600;
    }
    .relation-filter input { height: auto; }
    .graph-shell {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
    }
    #networkGraph { width: 100%; height: 780px; }
    .metrics {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      margin: 12px 0;
    }
    .metric-card {
      border: 1px solid var(--line);
      border-radius: 7px;
      padding: 12px;
      background: #fff;
    }
    .metric-card strong {
      display: block;
      color: var(--red);
      font-size: 20px;
    }
    .metric-card span {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }
    .analytics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }
    .analysis-card {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      padding: 12px;
      min-height: 360px;
      overflow: hidden;
    }
    .analysis-card h2 {
      margin: 0 0 8px;
      color: var(--red);
      font-size: 17px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      font-size: 12px;
    }
    th, td {
      border-bottom: 1px solid #ececec;
      padding: 7px 6px;
      text-align: left;
      vertical-align: top;
    }
    th { color: var(--muted); }
    @media (max-width: 760px) {
      .dashboard { grid-template-columns: 1fr; }
      .profile { border-right: 0; border-bottom: 1px solid var(--line); }
      .toolbar { grid-template-columns: 1fr 1fr; }
      .metrics { grid-template-columns: 1fr 1fr 1fr; }
      .analytics-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="dashboard">
    <aside class="profile">
      <h1>Suspect Profile</h1>
      <div class="search-row">
        <input id="suspectSearch" placeholder="Search suspect..." />
        <button id="searchBtn" title="Find suspect">Go</button>
      </div>
      <div class="photo" id="profilePhoto">CI</div>
      <section class="identity">
        <h2 id="profileName">Select a node</h2>
        <p id="profileAlias">Click any suspect to load intelligence profile.</p>
      </section>
      <div class="kv" id="profileFacts"></div>
      <h1 style="font-size:17px;margin-top:18px;">Centrality Scores</h1>
      <div id="profileScores"></div>
      <h1 style="font-size:17px;margin-top:18px;">Associations</h1>
      <div id="profileAssociations"></div>
    </aside>

    <main class="main">
      <h1>Criminal Network Analysis</h1>
      <section class="toolbar">
        <label>Community
          <select id="communityFilter"></select>
        </label>
        <label>Risk Level
          <select id="riskFilter">
            <option value="all">All</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </label>
        <label>Start Date
          <input type="date" id="startDate" />
        </label>
        <label>End Date
          <input type="date" id="endDate" />
        </label>
        <button id="resetFilters">Reset Filters</button>
        <div class="relation-filter" id="relationshipFilters"></div>
      </section>
      <section class="graph-shell">
        <div id="networkGraph"></div>
      </section>
      <section class="metrics" id="metricCards"></section>
      <section class="analytics-grid">
        <article class="analysis-card"><div id="sankeyGraph"></div></article>
        <article class="analysis-card"><div id="temporalGraph"></div></article>
        <article class="analysis-card"><div id="heatmapGraph"></div></article>
        <article class="analysis-card">
          <h2>Predictions, Paths, and Pattern Alerts</h2>
          <div id="predictionTables"></div>
        </article>
      </section>
    </main>
  </div>

  <script>
    const NODES = __NODES__;
    const EDGES = __EDGES__;
    const POSITIONS = __POSITIONS__;
    const METRICS = __METRICS__;
    const ROLE_COLORS = __ROLE_COLORS__;
    const COMMUNITY_COLORS = __COMMUNITY_COLORS__;
    const RELATIONSHIP_DASH = __RELATIONSHIP_DASH__;
    const SANKEY_FIG = __SANKEY_FIG__;
    const TEMPORAL_FIG = __TEMPORAL_FIG__;
    const HEATMAP_FIG = __HEATMAP_FIG__;
    const LINK_PREDICTIONS = __LINK_PREDICTIONS__;
    const SHORTEST_PATHS = __SHORTEST_PATHS__;

    function html(value) {
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
      })[char]);
    }

    function initials(name) {
      return String(name || "CI").split(" ").slice(0, 2).map((part) => part[0]).join("").toUpperCase();
    }

    function money(value) {
      return Number(value || 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });
    }

    function buildFilters() {
      const communities = [...new Set(NODES.map((node) => node.community))].sort((a, b) => a - b);
      document.getElementById("communityFilter").innerHTML =
        '<option value="all">All</option>' + communities.map((community) => `<option value="${community}">Community ${community}</option>`).join("");

      const types = [...new Set(EDGES.map((edge) => edge.relationship_type))].sort();
      document.getElementById("relationshipFilters").innerHTML = types.map((type) => `
        <label><input type="checkbox" value="${html(type)}" checked /> ${html(type)}</label>
      `).join("");

      const dates = EDGES.map((edge) => edge.occurred_on).sort();
      document.getElementById("startDate").value = dates[0];
      document.getElementById("endDate").value = dates[dates.length - 1];

      document.querySelectorAll("#communityFilter,#riskFilter,#startDate,#endDate").forEach((node) => {
        node.addEventListener("change", renderNetwork);
      });
      document.querySelectorAll("#relationshipFilters input").forEach((node) => node.addEventListener("change", renderNetwork));
      document.getElementById("resetFilters").addEventListener("click", () => {
        document.getElementById("communityFilter").value = "all";
        document.getElementById("riskFilter").value = "all";
        document.getElementById("startDate").value = dates[0];
        document.getElementById("endDate").value = dates[dates.length - 1];
        document.querySelectorAll("#relationshipFilters input").forEach((node) => { node.checked = true; });
        renderNetwork();
      });
      document.getElementById("searchBtn").addEventListener("click", searchSuspect);
      document.getElementById("suspectSearch").addEventListener("keydown", (event) => {
        if (event.key === "Enter") searchSuspect();
      });
    }

    function activeRelationshipTypes() {
      return new Set([...document.querySelectorAll("#relationshipFilters input:checked")].map((node) => node.value));
    }

    function getFilteredData() {
      const community = document.getElementById("communityFilter").value;
      const risk = document.getElementById("riskFilter").value;
      const start = document.getElementById("startDate").value;
      const end = document.getElementById("endDate").value;
      const relationshipTypes = activeRelationshipTypes();
      const visibleNodes = NODES.filter((node) => {
        if (community !== "all" && String(node.community) !== community) return false;
        if (risk !== "all" && node.risk_level !== risk) return false;
        return true;
      });
      const visibleIds = new Set(visibleNodes.map((node) => node.person_id));
      const visibleEdges = EDGES.filter((edge) => (
        visibleIds.has(edge.source)
        && visibleIds.has(edge.target)
        && relationshipTypes.has(edge.relationship_type)
        && edge.occurred_on >= start
        && edge.occurred_on <= end
      ));
      return { visibleNodes, visibleEdges };
    }

    function edgeHover(edge) {
      return `<b>${html(edge.relationship_type)}</b><br>${html(edge.source)} -> ${html(edge.target)}<br>` +
        `Weight: ${html(edge.weight)}<br>Date: ${html(edge.occurred_on)}<br>Amount INR: ${money(edge.amount_inr)}<extra></extra>`;
    }

    function nodeHover(node) {
      return `<b>${html(node.name)}</b><br>ID: ${html(node.person_id)}<br>Role: ${html(node.role)}<br>` +
        `Community: ${html(node.community)}<br>Risk: ${html(node.risk_score)} (${html(node.risk_level)})<br>` +
        `Degree: ${Number(node.degree_centrality).toFixed(3)}<br>` +
        `Betweenness: ${Number(node.betweenness_centrality).toFixed(3)}<br>` +
        `Closeness: ${Number(node.closeness_centrality).toFixed(3)}<br>` +
        `Eigenvector: ${Number(node.eigenvector_centrality).toFixed(3)}<br>` +
        `PageRank: ${Number(node.pagerank).toFixed(3)}<br>Anomaly: ${Number(node.anomaly_score).toFixed(1)}<extra></extra>`;
    }

    function renderNetwork() {
      const { visibleNodes, visibleEdges } = getFilteredData();
      const traces = [];
      visibleEdges.forEach((edge) => {
        const source = POSITIONS[edge.source];
        const target = POSITIONS[edge.target];
        const isMoneyChain = Boolean(edge.money_chain_id);
        traces.push({
          x: [source.x, target.x, null],
          y: [source.y, target.y, null],
          mode: "lines",
          type: "scatter",
          hovertemplate: edgeHover(edge),
          line: {
            width: 0.65 + Number(edge.weight) * 0.42 + (isMoneyChain ? 1.4 : 0),
            color: isMoneyChain ? "rgba(18,115,55,0.76)" : "rgba(0,0,0,0.50)",
            dash: RELATIONSHIP_DASH[edge.relationship_type] || "solid"
          },
          showlegend: false
        });
      });

      const byCommunity = {};
      visibleNodes.forEach((node) => {
        byCommunity[node.community] = byCommunity[node.community] || [];
        byCommunity[node.community].push(node);
      });
      Object.entries(byCommunity).forEach(([community, group]) => {
        traces.push({
          x: group.map((node) => POSITIONS[node.person_id].x),
          y: group.map((node) => POSITIONS[node.person_id].y),
          mode: "markers",
          type: "scatter",
          marker: {
            size: group.map((node) => 22 + Number(node.degree_centrality) * 58),
            color: COMMUNITY_COLORS[Number(community) % COMMUNITY_COLORS.length],
            opacity: 0.18,
            line: { width: 0 }
          },
          hoverinfo: "skip",
          showlegend: false
        });
      });

      const byRole = {};
      visibleNodes.forEach((node) => {
        byRole[node.role] = byRole[node.role] || [];
        byRole[node.role].push(node);
      });
      Object.entries(byRole).forEach(([role, group]) => {
        traces.push({
          x: group.map((node) => POSITIONS[node.person_id].x),
          y: group.map((node) => POSITIONS[node.person_id].y),
          text: group.map((node) => node.name),
          customdata: group.map((node) => node.person_id),
          mode: "markers+text",
          type: "scatter",
          name: role,
          textposition: "top center",
          textfont: { size: 9, color: "#111" },
          hovertemplate: group.map(nodeHover),
          marker: {
            size: group.map((node) => 12 + Number(node.degree_centrality) * 70),
            color: ROLE_COLORS[role] || "#546e7a",
            opacity: 0.95,
            line: {
              width: group.map((node) => node.is_key_influencer || node.is_bridge_node ? 4 : 2),
              color: group.map((node) => COMMUNITY_COLORS[Number(node.community) % COMMUNITY_COLORS.length])
            }
          }
        });
      });

      const layout = {
        paper_bgcolor: "white",
        plot_bgcolor: "white",
        margin: { l: 8, r: 8, t: 8, b: 8 },
        hovermode: "closest",
        showlegend: true,
        legend: { x: 0.01, y: 0.99, bgcolor: "rgba(255,255,255,0.86)", bordercolor: "#d8d8d8", borderwidth: 1 },
        xaxis: { visible: false, zeroline: false },
        yaxis: { visible: false, zeroline: false }
      };
      Plotly.react("networkGraph", traces, layout, { responsive: true, displaylogo: false });
      document.getElementById("networkGraph").on("plotly_click", (event) => {
        const point = event.points.find((item) => item.customdata);
        if (!point) return;
        const node = NODES.find((item) => item.person_id === point.customdata);
        if (node) showProfile(node);
      });
      renderMetricCards(visibleNodes, visibleEdges);
    }

    function renderMetricCards(nodes, edges) {
      const cards = [
        ["Density", METRICS.density],
        ["Diameter", METRICS.diameter],
        ["Avg Path Length", METRICS.average_path_length],
        ["Communities", METRICS.number_of_communities],
        ["Total Connections", METRICS.total_connections],
        ["Filtered Edges", edges.length]
      ];
      document.getElementById("metricCards").innerHTML = cards.map(([label, value]) => `
        <article class="metric-card"><strong>${html(value)}</strong><span>${html(label)}</span></article>
      `).join("");
    }

    function showProfile(node) {
      document.getElementById("profilePhoto").textContent = initials(node.name);
      document.getElementById("profileName").textContent = node.name;
      document.getElementById("profileAlias").textContent = `${node.alias} / ${node.role}`;
      document.getElementById("profileFacts").innerHTML = `
        <span>ID:</span><span>${html(node.person_id)}</span>
        <span>Risk score:</span><span>${html(node.risk_score)} / ${html(node.risk_level)}</span>
        <span>Known associates:</span><span>${html(node.known_associates)}</span>
        <span>Communications:</span><span>${html(node.number_of_communications)}</span>
        <span>Transactions:</span><span>${html(node.number_of_transactions)}</span>
        <span>Community:</span><span>${html(node.community)}</span>
        <span>District:</span><span>${html(node.district)}</span>
      `;
      const scores = [
        ["Degree", node.degree_centrality, "#1e88e5"],
        ["Betweenness", node.betweenness_centrality, "#fb8c00"],
        ["Closeness", node.closeness_centrality, "#2e7d32"],
        ["Eigenvector", node.eigenvector_centrality, "#e53935"],
        ["PageRank", node.pagerank, "#7b1fa2"],
        ["Anomaly", node.anomaly_score / 100, "#424242"]
      ];
      document.getElementById("profileScores").innerHTML = scores.map(([label, value, color]) => `
        <div class="score-row"><span><i class="dot" style="background:${color}"></i>${html(label)}</span><strong>${Number(value).toFixed(3)}</strong></div>
      `).join("");
      const badges = [
        node.is_key_influencer ? "Key influencer" : "",
        node.is_bridge_node ? "Bridge node" : "",
        node.is_isolated_cell ? "Isolated cell member" : "",
        node.is_money_laundering_chain ? "Money chain" : ""
      ].filter(Boolean);
      document.getElementById("profileAssociations").innerHTML = `
        <div class="kv">
          <span>Total money exposure:</span><span>INR ${money(node.money_total_inr)}</span>
          <span>External links:</span><span>${html(node.external_connections)}</span>
        </div>
        <div class="badge-row">${badges.map((badge) => `<span class="badge">${html(badge)}</span>`).join("") || '<span class="badge">No special flag</span>'}</div>
      `;
    }

    function searchSuspect() {
      const query = document.getElementById("suspectSearch").value.trim().toLowerCase();
      if (!query) return;
      const node = NODES.find((item) =>
        item.name.toLowerCase().includes(query)
        || item.alias.toLowerCase().includes(query)
        || item.person_id.toLowerCase().includes(query)
      );
      if (node) showProfile(node);
    }

    function renderTables() {
      const predictionRows = LINK_PREDICTIONS.slice(0, 10).map((row) => `
        <tr><td>${html(row.source)}</td><td>${html(row.target)}</td><td>${html(row.prediction_score)}</td><td>${html(row.shared_neighbors)}</td></tr>
      `).join("");
      const pathRows = SHORTEST_PATHS.slice(0, 8).map((row) => `
        <tr><td>${html(row.source)}</td><td>${html(row.target)}</td><td>${html(row.hop_count)}</td><td>${html(row.path)}</td></tr>
      `).join("");
      const anomalyRows = [...NODES].sort((a, b) => Number(b.anomaly_score) - Number(a.anomaly_score)).slice(0, 8).map((node) => `
        <tr><td>${html(node.person_id)}</td><td>${html(node.name)}</td><td>${html(node.role)}</td><td>${Number(node.anomaly_score).toFixed(1)}</td></tr>
      `).join("");
      document.getElementById("predictionTables").innerHTML = `
        <h3>Link Prediction</h3>
        <table><thead><tr><th>Source</th><th>Target</th><th>Score</th><th>Shared neighbors</th></tr></thead><tbody>${predictionRows}</tbody></table>
        <h3>Shortest Paths</h3>
        <table><thead><tr><th>Source</th><th>Target</th><th>Hops</th><th>Path</th></tr></thead><tbody>${pathRows}</tbody></table>
        <h3>Suspicious Anomaly Scores</h3>
        <table><thead><tr><th>ID</th><th>Name</th><th>Role</th><th>Score</th></tr></thead><tbody>${anomalyRows}</tbody></table>
      `;
    }

    buildFilters();
    renderNetwork();
    renderTables();
    showProfile([...NODES].sort((a, b) => Number(b.pagerank) - Number(a.pagerank))[0]);
    Plotly.newPlot("sankeyGraph", SANKEY_FIG.data, SANKEY_FIG.layout, { responsive: true, displaylogo: false });
    Plotly.newPlot("temporalGraph", TEMPORAL_FIG.data, TEMPORAL_FIG.layout, { responsive: true, displaylogo: false });
    Plotly.newPlot("heatmapGraph", HEATMAP_FIG.data, HEATMAP_FIG.layout, { responsive: true, displaylogo: false });
  </script>
</body>
</html>
"""
    replacements = {
        "__NODES__": to_json_records(nodes),
        "__EDGES__": to_json_records(edges),
        "__POSITIONS__": json.dumps(positions),
        "__METRICS__": json.dumps(metrics, default=str),
        "__ROLE_COLORS__": json.dumps(ROLE_COLORS),
        "__COMMUNITY_COLORS__": json.dumps(COMMUNITY_COLORS),
        "__RELATIONSHIP_DASH__": json.dumps(RELATIONSHIP_DASH),
        "__SANKEY_FIG__": json.dumps(sankey.to_plotly_json(), default=str),
        "__TEMPORAL_FIG__": json.dumps(temporal.to_plotly_json(), default=str),
        "__HEATMAP_FIG__": json.dumps(heatmap.to_plotly_json(), default=str),
        "__LINK_PREDICTIONS__": to_json_records(link_predictions),
        "__SHORTEST_PATHS__": to_json_records(shortest_paths),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def write_outputs(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    positions: dict[str, dict[str, float]],
    metrics: dict[str, Any],
    output_dir: Path,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    link_predictions = compute_link_predictions(nodes, edges)
    shortest_paths = compute_shortest_paths(nodes, edges)
    sankey = create_sankey_figure(nodes, edges)
    temporal = create_temporal_figure(edges)
    heatmap = create_heatmap_figure(nodes)

    html = render_dashboard_html(nodes, edges, positions, metrics, sankey, temporal, heatmap, link_predictions, shortest_paths)
    paths = {
        "html": output_dir / "criminal_network_dashboard.html",
        "png": output_dir / "criminal_network_dashboard.png",
        "nodes_csv": output_dir / "criminal_nodes.csv",
        "edges_csv": output_dir / "criminal_edges.csv",
        "metrics_json": output_dir / "criminal_network_metrics.json",
        "link_predictions_csv": output_dir / "link_predictions.csv",
        "shortest_paths_csv": output_dir / "shortest_paths.csv",
    }
    paths["html"].write_text(html, encoding="utf-8")
    nodes.to_csv(paths["nodes_csv"], index=False)
    edges.to_csv(paths["edges_csv"], index=False)
    link_predictions.to_csv(paths["link_predictions_csv"], index=False)
    shortest_paths.to_csv(paths["shortest_paths_csv"], index=False)
    paths["metrics_json"].write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    write_static_network_png(nodes, edges, positions, paths["png"])
    return paths


def build_dashboard(config: DashboardConfig) -> dict[str, Path]:
    nodes = make_synthetic_nodes(config)
    edges = make_synthetic_edges(nodes, config)
    nodes, edges, metrics = enrich_network(nodes, edges, config)
    positions = compute_layout(nodes, edges, config.seed)
    return write_outputs(nodes, edges, positions, metrics, config.output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a criminal network analysis dashboard.")
    parser.add_argument("--nodes", type=int, default=100, help="Number of synthetic intelligence nodes.")
    parser.add_argument("--edges", type=int, default=250, help="Number of synthetic relationship edges.")
    parser.add_argument("--seed", type=int, default=20260609, help="Random seed for reproducible output.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/criminal_network"), help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.nodes != 100:
        raise ValueError("This dashboard role distribution is calibrated for exactly 100 nodes.")
    config = DashboardConfig(node_count=args.nodes, edge_count=args.edges, seed=args.seed, output_dir=args.output_dir)
    paths = build_dashboard(config)
    print("Generated criminal network dashboard artifacts:")
    for label, path in paths.items():
        print(f"- {label}: {path.resolve()}")


if __name__ == "__main__":
    main()
