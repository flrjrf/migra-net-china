# China Mobility Network

This repository explores **internal migration flows across China** through the lens of **network science** and **complex systems theory**.  
Using spatial and survey data (CMDS 2017), it models population movements as a **directed weighted network**, where nodes represent administrative regions and edges represent migration links.

---

## 🧠 Project Overview

The main objectives of this project are:

- To **visualize** migration flows between Chinese provinces, prefectures, and counties.
- To **model** the structure of these flows using **network science** tools.
- To analyze **centrality, connectivity, and rich-club phenomena** within the migration network.
- To draw parallels between human migration systems and **logistics or transportation networks**, such as China's railway system.

---

## ⚙️ Data

- **Source:** China Migrant Dynamic Survey (CMDS), 2017.  
- **Geospatial data:** Administrative boundaries from the [`mapchina`](https://cran.r-project.org/package=mapchina) package.  
- **Main variables used:**
  - `C1`, `C2`, `C3` – origin province, prefecture, and county codes.
  - `q101j1a` – destination county code.

> Note: Raw datasets are not included in this repository.

---

## 🧩 Methodology

1. **Preprocessing**
   - Join migration records with spatial geometries.
   - Filter and clean missing or invalid coordinates.

2. **Network Construction**
   - Represent each county as a node.
   - Add edges representing migration from origin to destination.
   - Weight edges by number of migrants.

3. **Analysis**
   - Compute network metrics (degree, betweenness, clustering, assortativity).
   - Identify **rich-club structures** to reveal hierarchical connectivity.
   - Explore correlations with transport infrastructure (e.g., high-speed rail).

4. **Visualization**
   - Plot migration flows using `ggplot2` and spatial layers.
   - Optionally rasterize heavy plots using `ggrastr` for efficiency.

---

## 📦 Folder Structure

