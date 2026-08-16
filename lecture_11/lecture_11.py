# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lecture 11: Working with Research Data - File Formats and Databases
#
#
# ## Quick Access
#
# Scan the QR codes below for quick access to course materials:
#
# <div style="display: flex; gap: 20px; align-items: flex-start;">
#   <div style="text-align: center;">
#     <img src="../course_qr_code.png" alt="Course Website QR Code" width="150"/>
#     <p><strong>Course Website</strong></p>
#   </div>
#   <div style="text-align: center;">
#     <img src="lecture_11_qr_code.png" alt="This Lecture QR Code" width="150"/>
#     <p><strong>This Lecture</strong></p>
#   </div>
# </div>
#
# ## Overview
# Research data is at the heart of scientific discovery. How you store, access, and
# share your data can make the difference between reproducible science and lost
# knowledge. This lecture explores best practices for managing research data through
# appropriate file formats and storage solutions. We'll ground our discussion in the
# FAIR principles (Findable, Accessible, Interoperable, Reusable) and demonstrate
# practical implementations with real-world examples.
#
# **Duration**: ~90 minutes
#
# ## Prerequisites
#
# Before starting this lecture, you should be familiar with:
# - Python file I/O operations (covered in Lecture 3)
# - NumPy for numerical data (covered in Lecture 4)
# - Basic understanding of data analysis workflows
# - Pandas basics (helpful but not required)
#
# This lecture introduces research data management best practices and specialized file formats.
#
# ## Learning Objectives
# - Understand FAIR principles and their application to research data
# - Learn about Research Data Management (RDM) best practices
# - Recognize FAIR4RS principles for research software
# - Choose appropriate file formats for different data types
# - Work with scientific file formats (HDF5, NetCDF)
# - Use databases effectively for structured research data
# - Implement data validation and integrity checking
# - Apply these concepts across different programming languages

# %% [markdown]
# ## Part 1: FAIR Principles and Research Data Management
#
# ### The Data Crisis in Research
#
# Dr. Maria Santos made a troubling discovery. Three years after publishing her
# groundbreaking climate study, another researcher asked for the raw data to build
# on her findings. Maria searched everywhere:
# - The external hard drive? Corrupted.
# - The lab server? Reorganized, files lost.
# - Her old laptop? Recycled two years ago.
# - Email attachments? Buried in 50,000 messages.
# - The data? **Gone forever**.
#
# Her published results couldn't be verified. Her follow-up study was impossible.
# Years of work, reduced to unreproducible claims.
#
# **This happens more often than you think.**
#
# ### Enter FAIR Principles
#
# In 2016, researchers formalized principles that data should be:
#
# **F - Findable**
# - Assigned a persistent identifier (DOI, Handle, PURL)
# - Described with rich metadata
# - Registered in a searchable resource
#
# **A - Accessible**
# - Retrievable via standardized protocols (HTTP, FTP, etc.)
# - Metadata remains accessible even if data is restricted
# - Clear access conditions and authentication procedures
#
# **I - Interoperable**
# - Uses formal, shared vocabularies
# - Includes references to other data/metadata
# - Follows community standards
#
# **R - Reusable**
# - Well-described with attributes
# - Released with clear usage license
# - Associated with detailed provenance
# - Meets domain-relevant community standards
#
# **Reference**: Wilkinson et al. (2016), "The FAIR Guiding Principles for
# scientific data management and stewardship", *Scientific Data*, 3:160018.
# DOI: 10.1038/sdata.2016.18
#
# ### Research Data Management (RDM)
#
# Research Data Management is the active organization and maintenance of data
# throughout the research lifecycle:
#
# **1. Planning Phase**
# - Create a Data Management Plan (DMP)
# - Identify data types and volumes
# - Choose file formats and standards
# - Determine storage and backup strategies
# - Plan for long-term preservation
#
# **2. Active Research Phase**
# - Organize data with clear naming conventions
# - Document data collection methods
# - Implement version control for data
# - Regular backups (3-2-1 rule: 3 copies, 2 media types, 1 off-site)
# - Quality assurance and validation
#
# **3. Publishing and Sharing Phase**
# - Deposit in appropriate repository
# - Assign persistent identifiers
# - Create comprehensive metadata
# - Choose appropriate license
# - Link to publications
#
# **4. Long-term Preservation**
# - Use archival formats
# - Migrate to new formats as needed
# - Maintain documentation
#
# ### FAIR4RS: FAIR for Research Software
#
# The FAIR principles were extended to research software through the FAIR4RS
# initiative (FAIR for Research Software). Key adaptations include:
#
# **Software-specific considerations:**
# - **Findable**: Registered in software registries, has citation metadata
# - **Accessible**: Available via version control, has installation instructions
# - **Interoperable**: Uses standard formats, documented dependencies and interfaces
# - **Reusable**: Licensed, documented, follows coding standards
#
# The connection to data management: **good software enables FAIR data**.
# - Software that writes well-structured data files helps Interoperability
# - Software with proper metadata supports Findability
# - Open-source tools ensure Accessibility
# - Well-documented code enables Reusability
#
# **Reference**: Barker et al. (2022), "Introducing the FAIR Principles for
# research software", *Scientific Data*, 9:622. DOI: 10.1038/s41597-022-01710-x
#
# ### Practical FAIR Implementation
#
# Let's see how FAIR principles guide data format choices:

# %%
# Example: Adding FAIR metadata to a simple dataset
import json
import datetime

# Non-FAIR approach - just the data
temperature_data = [15.2, 16.1, 14.8, 15.9, 16.3]

# FAIR approach - data WITH metadata
fair_data = {
    "metadata": {
        "title": "Daily Temperature Measurements - Campus Weather Station",
        "identifier": "10.5281/zenodo.1234567",  # Persistent identifier (DOI)
        "creator": "Dr. Maria Santos",
        "created": "2026-02-01",
        "modified": datetime.datetime.now().isoformat(),
        "description": "Temperature measurements taken at 12:00 UTC daily",
        "keywords": ["temperature", "meteorology", "climate"],
        "license": "CC-BY-4.0",
        "access_rights": "open",
        "temporal_coverage": "2026-02-01/2026-02-05",
        "spatial_coverage": "52.5200°N, 13.4050°E",  # Berlin coordinates
        "units": "degrees_Celsius",
        "measurement_technique": "PT100 RTD sensor, accuracy ±0.1°C",
        "instrument": "Vaisala HMP155",
        "related_publication": "10.1234/journal.2026.123",
    },
    "data": {"dates": ["2026-02-01", "2026-02-02", "2026-02-03", "2026-02-04", "2026-02-05"], "temperature": temperature_data},
}

print("FAIR metadata example:")
print(json.dumps(fair_data["metadata"], indent=2)[:500] + "...")

# %% [markdown]
# **Why this matters:**
# - Future researchers can **find** this data via the DOI
# - They can **access** it with clear license terms
# - They understand the **interoperable** format and units
# - They can **reuse** it knowing the methodology and provenance

# %% [markdown]
# ## Part 2: Choosing the Right File Format
#
# ### The Format Matters
#
# Different research data requires different storage formats. Your choice affects:
# - **Performance**: Read/write speed, memory usage
# - **Storage**: File size, compression
# - **Interoperability**: Can others read your data?
# - **Longevity**: Will this format exist in 10 years?
# - **Features**: Metadata, compression, partial I/O, parallel access
#
# ### Common Research Data Scenarios
#
# Let's explore formats for different use cases:
#
# **1. Tabular Data** (observations, measurements, survey results)
# - **CSV**: Universal, human-readable, no metadata
# - **Excel**: Convenient, not ideal for large data or automation
# - **Parquet**: Columnar storage, excellent compression, fast queries
# - **HDF5/NetCDF**: Great for large tables with metadata
#
# **2. Multidimensional Arrays** (climate models, medical imaging, simulations)
# - **HDF5**: Hierarchical data, compression, partial I/O
# - **NetCDF**: Climate/ocean data standard, built on HDF5
# - **Zarr**: Cloud-optimized chunked arrays
#
# **3. Time Series** (sensor data, stock prices, physiological signals)
# - **HDF5/NetCDF**: With time dimension
# - **Parquet**: Efficient for queries
# - **Specialized**: InfluxDB, TimescaleDB
#
# **4. Relational Data** (structured records with relationships)
# - **SQLite**: Single-file database, no server needed
# - **PostgreSQL/MySQL**: Multi-user, server-based
#
# **5. Configuration and Metadata**
# - **JSON**: Widely supported, human-readable
# - **YAML**: More readable for configs
# - **TOML**: Clean, unambiguous
#
# ### Format Selection Decision Tree
#
# ```
# Start: What type of data do you have?
#   │
#   ├─> Simple table, small size (<100 MB)
#   │   └─> Use CSV (universal compatibility)
#   │
#   ├─> Table with complex types or large size
#   │   └─> Use Parquet or HDF5
#   │
#   ├─> Multidimensional scientific arrays
#   │   ├─> Climate/ocean/atmosphere data? → NetCDF
#   │   └─> Other scientific arrays → HDF5
#   │
#   ├─> Relational data with queries
#   │   ├─> Single user, portable? → SQLite
#   │   └─> Multi-user, server? → PostgreSQL
#   │
#   └─> Metadata/configuration
#       └─> JSON or YAML
# ```

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Curious about data formats in practice? Explore these hands-on activities:</p>
#     <ul>
#         <li><strong>Benchmark your data</strong>: Take a dataset you work with and save
#         it as CSV, JSON, and pickle. Compare file sizes and read/write speeds. Which
#         format wins for your use case?</li>
#         <li><strong>Test data validation</strong>: Intentionally corrupt a data file (wrong
#         data type, missing value, out-of-range number). Does your code catch it? Add
#         validation that would!</li>
#         <li><strong>Think about 10 years from now</strong>: Which format would you trust
#         to be readable in a decade? Try opening a 10-year-old Excel file or CSV - what
#         happened to it?</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 3: Working with HDF5 - Hierarchical Data Format
#
# ### What is HDF5?
#
# HDF5 (Hierarchical Data Format version 5) is a file format designed for storing
# and organizing large amounts of scientific data. Think of it as a **file system
# within a file**.
#
# **Key features:**
# - Stores heterogeneous data (arrays, tables, metadata) in one file
# - Hierarchical organization (groups like directories, datasets like files)
# - Efficient compression
# - Partial I/O (read subset without loading entire file)
# - Supports very large datasets (terabytes+)
# - Self-describing with embedded metadata
# - Platform independent (binary format with libraries for all major languages)
#
# **Who uses HDF5?**
# - Climate science (CMIP6 climate models)
# - Particle physics (LHC data)
# - Astronomy (telescope data)
# - Medical imaging (MRI, CT scans)
# - Machine learning (large training datasets)
#
# ### HDF5 Structure
#
# ```
# climate_data.h5
# ├─ /metadata
# │  ├─ institution: "Max Planck Institute"
# │  ├─ contact: "research@example.org"
# │  └─ created: "2026-01-15"
# ├─ /experiment_001
# │  ├─ temperature [365, 180, 360]  # 3D array: time, lat, lon
# │  ├─ pressure [365, 180, 360]
# │  └─ metadata
# │     ├─ description: "RCP8.5 scenario simulation"
# │     └─ units: {"temperature": "K", "pressure": "Pa"}
# └─ /experiment_002
#    └─ ...
# ```

# %% [markdown]
# ### Practical Example: Climate Data with HDF5
#
# Let's create a realistic research data file using HDF5:

# %%
import h5py
import numpy as np
import tempfile
import os

# Create a realistic climate dataset
# Dimensions: time (365 days), latitude (180), longitude (360)
np.random.seed(42)

# Use cross-platform temporary directory
temp_dir = tempfile.gettempdir()
hdf5_file = os.path.join(temp_dir, "climate_simulation.h5")

# Simulate temperature data (in Kelvin, typical range 200-320K)
time_steps = 365
n_lat = 180
n_lon = 360

# Base temperature field with realistic spatial variation
lat = np.linspace(-90, 90, n_lat)
lon = np.linspace(-180, 180, n_lon)

# Create latitude-dependent base temperature (warmer at equator)
lat_effect = 288 - 30 * np.abs(lat / 90.0)  # 258-288K range
base_temp = lat_effect[:, np.newaxis] * np.ones((n_lat, n_lon))

# Add temporal variation (seasonal cycle)
time = np.arange(time_steps)
seasonal = 10 * np.sin(2 * np.pi * time / 365.0)  # ±10K seasonal variation

# Combine: 3D array (time, lat, lon)
temperature = base_temp[np.newaxis, :, :] + seasonal[:, np.newaxis, np.newaxis]
# Add small random noise
temperature += np.random.randn(time_steps, n_lat, n_lon) * 0.5

print(f"Temperature data shape: {temperature.shape}")
print(f"Temperature range: {temperature.min():.1f} - {temperature.max():.1f} K")
print(f"Memory size: {temperature.nbytes / 1e6:.1f} MB")

# %% [markdown]
# Now let's save this data in a FAIR-compliant HDF5 file:

# %%
# Create HDF5 file with comprehensive metadata
with h5py.File(hdf5_file, "w") as f:
    # Root-level metadata (FAIR principles)
    f.attrs["title"] = "Climate Model Simulation - Temperature Data"
    f.attrs["institution"] = "Research Software Engineering Course"
    f.attrs["creator"] = "Lecture 11 Example"
    f.attrs["created"] = "2026-02-10"
    f.attrs["version"] = "1.0"
    f.attrs["license"] = "CC-BY-4.0"
    f.attrs["description"] = "Daily global temperature simulation from a " "simplified climate model"
    f.attrs["conventions"] = "CF-1.8"  # Climate and Forecast conventions

    # Create groups for organization (like directories)
    model_group = f.create_group("model_output")
    coord_group = f.create_group("coordinates")

    # Store the temperature data with compression
    temp_dataset = model_group.create_dataset(
        "temperature",
        data=temperature,
        compression="gzip",
        compression_opts=6,  # Compression level 1-9
        chunks=(30, 90, 180),  # Chunk size for efficient partial I/O
    )

    # Dataset-specific metadata
    temp_dataset.attrs["units"] = "Kelvin"
    temp_dataset.attrs["long_name"] = "Surface Air Temperature"
    temp_dataset.attrs["standard_name"] = "air_temperature"
    temp_dataset.attrs["valid_range"] = [0, 350]
    temp_dataset.attrs["missing_value"] = -999.0

    # Store coordinate information
    coord_group.create_dataset("time", data=time)
    coord_group.create_dataset("latitude", data=lat)
    coord_group.create_dataset("longitude", data=lon)

    # Add coordinate metadata
    coord_group["time"].attrs["units"] = "days since 2026-01-01"
    coord_group["time"].attrs["calendar"] = "gregorian"
    coord_group["latitude"].attrs["units"] = "degrees_north"
    coord_group["longitude"].attrs["units"] = "degrees_east"

print(f"✅ HDF5 file created: {hdf5_file}")

# Check the file size
file_size = os.path.getsize(hdf5_file) / 1e6
print(f"File size: {file_size:.1f} MB (compressed from {temperature.nbytes/1e6:.1f} MB)")
print(f"Compression ratio: {temperature.nbytes / os.path.getsize(hdf5_file):.1f}x")

# %% [markdown]
# ### Reading and Working with HDF5 Data

# %%
# Read the HDF5 file
with h5py.File(hdf5_file, "r") as f:
    # Explore the file structure
    print("File structure:")
    print(f"  Root attributes: {list(f.attrs.keys())}")
    print(f"  Groups: {list(f.keys())}")

    # Access metadata (FAIR Findability)
    print(f"\nTitle: {f.attrs['title']}")
    print(f"License: {f.attrs['license']}")
    print(f"Description: {f.attrs['description']}")

    # Navigate hierarchy
    temp = f["model_output/temperature"]
    print(f"\nTemperature dataset:")
    print(f"  Shape: {temp.shape}")
    print(f"  Units: {temp.attrs['units']}")
    print(f"  Standard name: {temp.attrs['standard_name']}")

    # Partial I/O - read only a subset (very efficient for large files!)
    # Get temperature for first week at equator
    subset = temp[0:7, 90, :]  # First 7 days, equator (lat index 90), all longitudes
    print(f"\nPartial read (first week at equator):")
    print(f"  Shape: {subset.shape}")
    print(f"  Mean temperature: {subset.mean():.1f} K ({subset.mean() - 273.15:.1f} °C)")

# %% [markdown]
# **Key advantages demonstrated:**
# 1. **Metadata embedded** - File is self-documenting (FAIR Interoperable)
# 2. **Compression** - 3-4x smaller than raw data
# 3. **Partial I/O** - Read subset without loading 100+ MB into memory
# 4. **Organization** - Hierarchical groups keep related data together
# 5. **Standards** - CF conventions ensure interoperability with other tools
#
# **Cross-language support:**
# - **Python**: h5py, PyTables
# - **R**: rhdf5, hdf5r
# - **MATLAB**: built-in HDF5 support (h5read, h5write)
# - **Julia**: HDF5.jl
# - **C/C++/Fortran**: Native HDF5 library
# - **Java**: HDF5-Java library

# %% [markdown]
# ## Part 4: NetCDF - Network Common Data Form
#
# ### What is NetCDF?
#
# NetCDF is a file format specifically designed for array-oriented scientific data,
# particularly popular in atmospheric and ocean sciences. It's built on HDF5 but
# adds domain-specific conventions.
#
# **Key features:**
# - Self-describing: includes metadata with data
# - Portable: platform-independent
# - Appendable: can add data efficiently
# - Supports Climate and Forecast (CF) conventions
# - Direct access: efficient reading of data subsets
# - Standard for climate modeling (CMIP, IPCC reports use NetCDF)
#
# **NetCDF vs HDF5:**
# - NetCDF4 uses HDF5 as backend (NetCDF3 is older, different format)
# - NetCDF provides higher-level, domain-specific interface
# - NetCDF enforces certain conventions (dimensions, coordinates, variables)
# - HDF5 is more general-purpose and flexible
# - For climate/ocean/atmosphere data: use NetCDF
# - For other scientific data: HDF5 is often better

# %% [markdown]
# ### Practical Example: Creating CF-Compliant NetCDF
#
# **Note:** The following code demonstrates how to create NetCDF files. Due to
# potential HDF5 library version conflicts in some environments, the actual file
# creation may not execute. The code structure and approach are what matters for
# learning purposes.

# %%
from netCDF4 import Dataset
import numpy as np

# This demonstrates the structure for creating a NetCDF file following CF conventions
# In production, ensure compatible versions of netCDF4 and HDF5 libraries

print("NetCDF File Creation Example:")
print("=" * 50)
print("""
# Example NetCDF file creation structure:

nc_file = Dataset('ocean_temperature.nc', 'w', format='NETCDF4')

# Global attributes (FAIR metadata)
nc_file.title = "Ocean Temperature Observations"
nc_file.institution = "Marine Research Institute"
nc_file.Conventions = "CF-1.8"
nc_file.license = "CC-BY-4.0"

# Create dimensions
time_dim = nc_file.createDimension('time', None)  # unlimited
depth_dim = nc_file.createDimension('depth', 50)
lat_dim = nc_file.createDimension('lat', 1)
lon_dim = nc_file.createDimension('lon', 1)

# Create coordinate variables with metadata
depth_var = nc_file.createVariable('depth', 'f4', ('depth',))
depth_var.units = 'meters'
depth_var.positive = 'down'
depth_var.standard_name = 'depth'

# Create data variable with compression
temp_var = nc_file.createVariable(
    'temperature', 'f4', ('time', 'depth', 'lat', 'lon'),
    compression='zlib', complevel=6
)
temp_var.units = 'degrees_Celsius'
temp_var.standard_name = 'sea_water_temperature'

# Fill with data
depth_var[:] = np.linspace(0, 500, 50)
temp_var[0, :, 0, 0] = 22 - depth_var[:] / 50  # Thermocline

nc_file.close()
""")

# %% [markdown]
# ### Reading NetCDF Files
#
# **Note:** This section demonstrates how to read NetCDF files. The actual execution
# depends on having a properly created NetCDF file and compatible library versions.

# %%
# Example of reading a NetCDF file structure
print("NetCDF File Reading Example:")
print("=" * 50)
print("""
# Reading NetCDF files:

nc = Dataset('ocean_temperature.nc', 'r')

# Explore file structure
print("Dimensions:", list(nc.dimensions.keys()))
print("Variables:", list(nc.variables.keys()))

# Access global attributes (FAIR metadata)
print("Title:", nc.title)
print("Institution:", nc.institution)
print("License:", nc.license)

# Access data variables
temp = nc.variables['temperature']
print("Temperature shape:", temp.shape)
print("Temperature units:", temp.units)
print("Standard name:", temp.standard_name)

# Efficient subset reading
surface_temp = temp[:, 0, 0, 0]  # Surface only
temp_at_100m = temp[:, 20, 0, 0]  # ~100m depth

# Don't forget to close
nc.close()
""")

# %% [markdown]
# **Why NetCDF is excellent for research:**
# 1. **Community standard** - Climate researchers worldwide use it (FAIR Interoperable)
# 2. **Self-describing** - Metadata travels with data (FAIR Findable)
# 3. **CF conventions** - Standardized names and units (FAIR Interoperable)
# 4. **Tool support** - Hundreds of tools can read NetCDF (FAIR Accessible)
# 5. **Efficient** - Compression and partial I/O
#
# **Cross-language support:**
# - **Python**: netCDF4-python, xarray (high-level)
# - **R**: ncdf4, RNetCDF
# - **MATLAB**: Built-in support (ncread, ncwrite)
# - **Julia**: NetCDF.jl
# - **C/Fortran**: Native NetCDF library
# - **IDL**: Built-in NetCDF support
# - **NCO/CDO**: Command-line tools for NetCDF manipulation

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Want to master scientific data formats? Try these comparative experiments:</p>
#     <ul>
#         <li><strong>Convert between formats</strong>: Take data in CSV and convert it to
#         HDF5, then to NetCDF. What metadata can you preserve? What gets lost? Which
#         format feels most natural for your data?</li>
#         <li><strong>Explore compression</strong>: Save the same array in HDF5 with
#         different compression levels. How much space do you save? How much slower is
#         reading? Find the sweet spot for your data.</li>
#         <li><strong>Read a subset</strong>: Load just one variable from a multi-variable
#         HDF5/NetCDF file, or just rows 1000-2000 from a million-row dataset. Experience
#         the power of partial I/O!</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 5: Databases for Research Data
#
# ### When to Use a Database
#
# **Use a database when you have:**
# - Structured data with complex relationships
# - Need for concurrent access by multiple users
# - Frequent queries with different criteria
# - Transactional requirements (data integrity critical)
# - Data that changes frequently
#
# **Don't use a database when:**
# - Simple file I/O is sufficient
# - Data is primarily large arrays (use HDF5/NetCDF)
# - Single-user, read-only access
# - Need maximum portability (single file preferred)
#
# ### SQLite: The Research-Friendly Database
#
# SQLite is perfect for research because:
# - **Single file** - entire database in one portable file
# - **No server** - embedded database, no setup required
# - **ACID compliant** - data integrity guaranteed
# - **Cross-platform** - works everywhere
# - **Self-contained** - no dependencies
# - **Public domain** - completely free
#
# **Common research uses:**
# - Experimental metadata and results
# - Survey responses
# - Observation logs
# - Sample tracking
# - Literature databases
# - Any structured tabular data with relationships

# %% [markdown]
# ### Practical Example: Experimental Results Database
#
# Let's create a database for a materials science experiment:

# %%
import sqlite3
import json
import os
import tempfile

# Use cross-platform temporary directory
temp_dir = tempfile.gettempdir()
db_file = os.path.join(temp_dir, "materials_experiments.db")

# Remove old database if it exists to ensure clean run
if os.path.exists(db_file):
    os.remove(db_file)

# Create database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create tables with proper schema
cursor.execute("""
CREATE TABLE experiments (
    experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_name TEXT NOT NULL,
    researcher TEXT NOT NULL,
    date_conducted TEXT NOT NULL,
    temperature REAL,
    pressure REAL,
    notes TEXT,
    metadata TEXT,  -- JSON for flexible metadata
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER NOT NULL,
    measurement_time REAL NOT NULL,
    property_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    uncertainty REAL,
    FOREIGN KEY (experiment_id) REFERENCES experiments (experiment_id)
)
""")

# Create index for fast queries
cursor.execute("""
CREATE INDEX idx_experiment_date ON experiments(date_conducted)
""")

cursor.execute("""
CREATE INDEX idx_measurement_property ON measurements(property_name)
""")

# Insert sample experiments with FAIR metadata
experiments = [
    {
        "experiment_name": "Graphene_Synthesis_001",
        "researcher": "Dr. Chen",
        "date_conducted": "2026-02-01",
        "temperature": 1200.0,
        "pressure": 0.001,
        "notes": "Initial synthesis test with optimal parameters",
        "metadata": json.dumps(
            {
                "doi": "10.5281/zenodo.experiment001",
                "protocol": "CVD_standard_v2.1",
                "substrate": "copper_foil",
                "gas_mixture": {"CH4": 0.05, "H2": 0.95},
            }
        ),
    },
    {
        "experiment_name": "Graphene_Synthesis_002",
        "researcher": "Dr. Chen",
        "date_conducted": "2026-02-03",
        "temperature": 1150.0,
        "pressure": 0.001,
        "notes": "Lower temperature test",
        "metadata": json.dumps(
            {
                "doi": "10.5281/zenodo.experiment002",
                "protocol": "CVD_standard_v2.1",
                "substrate": "copper_foil",
                "gas_mixture": {"CH4": 0.05, "H2": 0.95},
            }
        ),
    },
]

for exp in experiments:
    cursor.execute(
        """
        INSERT INTO experiments 
        (experiment_name, researcher, date_conducted, temperature, pressure, notes, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            exp["experiment_name"],
            exp["researcher"],
            exp["date_conducted"],
            exp["temperature"],
            exp["pressure"],
            exp["notes"],
            exp["metadata"],
        ),
    )

# Insert measurements for experiment 1
measurements_exp1 = [
    (1, 0.0, "thickness", 1.2, "nanometers", 0.1),
    (1, 0.5, "thickness", 1.5, "nanometers", 0.1),
    (1, 1.0, "thickness", 2.1, "nanometers", 0.1),
    (1, 0.0, "conductivity", 850, "S/m", 50),
    (1, 1.0, "conductivity", 920, "S/m", 50),
]

for meas in measurements_exp1:
    cursor.execute(
        """
        INSERT INTO measurements 
        (experiment_id, measurement_time, property_name, value, unit, uncertainty)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        meas,
    )

conn.commit()
print("✅ Database created with experiments and measurements")

# %% [markdown]
# ### Querying the Database

# %%
# Query 1: Get all experiments by date
cursor.execute("""
    SELECT experiment_name, researcher, date_conducted, temperature
    FROM experiments
    ORDER BY date_conducted
""")

print("All experiments:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[2]}, {row[3]}K by {row[1]}")

# Query 2: Get average thickness over time for experiment 1
cursor.execute("""
    SELECT measurement_time, AVG(value) as avg_thickness, AVG(uncertainty) as avg_uncertainty
    FROM measurements
    WHERE experiment_id = 1 AND property_name = 'thickness'
    GROUP BY measurement_time
    ORDER BY measurement_time
""")

print("\nThickness evolution (Experiment 1):")
for row in cursor.fetchall():
    print(f"  Time {row[0]:.1f}h: {row[1]:.2f} ± {row[2]:.2f} nm")

# Query 3: Find experiments with temperature above 1175K
cursor.execute("""
    SELECT experiment_name, temperature, pressure
    FROM experiments
    WHERE temperature > 1175
""")

print("\nHigh-temperature experiments:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}K, {row[2]} Pa")

# Query 4: Get metadata for specific experiment
cursor.execute("""
    SELECT metadata FROM experiments WHERE experiment_name = 'Graphene_Synthesis_001'
""")
metadata_json = cursor.fetchone()[0]
metadata = json.loads(metadata_json)
print(f"\nExperiment metadata:")
print(f"  DOI: {metadata['doi']}")
print(f"  Protocol: {metadata['protocol']}")
print(f"  Substrate: {metadata['substrate']}")

conn.close()

# %% [markdown]
# **Database advantages for research:**
# 1. **Relationships** - Link experiments to measurements properly
# 2. **Queries** - Find data matching complex criteria
# 3. **Integrity** - Foreign keys prevent orphaned data
# 4. **ACID transactions** - Data consistency guaranteed
# 5. **Flexible metadata** - JSON fields for variable metadata
# 6. **Portable** - Single file contains everything
#
# **Cross-language support:**
# - **Python**: sqlite3 (built-in), sqlalchemy (ORM)
# - **R**: RSQLite, DBI
# - **MATLAB**: Database Toolbox supports SQLite
# - **Julia**: SQLite.jl
# - **C/C++**: Native SQLite library
# - **Java**: JDBC SQLite driver
# - **JavaScript/Node.js**: better-sqlite3, sql.js

# %% [markdown]
# <div style="background-color: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; margin: 10px 0; border-radius: 5px;">
#     <h4 style="color: #7b1fa2; margin-top: 0;">💡 Try It Yourself</h4>
#     <p>Ready to think like a database designer? Try these schema explorations:</p>
#     <ul>
#         <li><strong>Design your research schema</strong>: Take a research project you're
#         working on. What are the entities (experiments, samples, measurements)? How do
#         they relate? Sketch a simple schema with 3-4 tables.</li>
#         <li><strong>CSV vs. SQLite showdown</strong>: Convert a multi-file CSV dataset
#         into a SQLite database with proper relationships. Which is easier to query? Which
#         is easier to maintain?</li>
#         <li><strong>Practice SQL queries</strong>: Using your data, write queries that
#         join tables, filter results, and aggregate values. SQL is powerful once you get
#         comfortable with it!</li>
#     </ul>
# </div>

# %% [markdown]
# ## Part 6: Data Validation and Quality Assurance
#
# ### Why Validation Matters
#
# Research data without quality checks is a ticking time bomb:
# - **Garbage in, garbage out** - Invalid data produces invalid results
# - **Silent errors** - Bad data might not cause crashes, just wrong conclusions
# - **Reproducibility** - Others can't reproduce results from corrupted data
# - **Wasted time** - Discovering data issues months later wastes effort
#
# ### Validation Strategies
#
# **1. Range Checks**


# %%
def validate_temperature_data(temperature, min_valid=-100, max_valid=60):
    """Validate temperature data is in reasonable range for Earth surface.

    Args:
        temperature: Array of temperature values in Celsius
        min_valid: Minimum valid temperature (default: -100°C)
        max_valid: Maximum valid temperature (default: 60°C)

    Returns:
        dict with validation results
    """
    import numpy as np

    temp_array = np.asarray(temperature)

    # Check for NaN/Inf
    n_nan = np.isnan(temp_array).sum()
    n_inf = np.isinf(temp_array).sum()

    # Check range
    below_min = (temp_array < min_valid).sum()
    above_max = (temp_array > max_valid).sum()

    # Statistics
    if len(temp_array) > 0:
        mean_temp = np.nanmean(temp_array)
        std_temp = np.nanstd(temp_array)
    else:
        mean_temp = std_temp = np.nan

    # Check all validity conditions
    all_conditions = [n_nan == 0, n_inf == 0, below_min == 0, above_max == 0]
    valid = all(all_conditions)

    return {
        "valid": valid,
        "n_points": len(temp_array),
        "n_nan": n_nan,
        "n_inf": n_inf,
        "n_below_min": below_min,
        "n_above_max": above_max,
        "mean": mean_temp,
        "std": std_temp,
        "min": np.nanmin(temp_array) if len(temp_array) > 0 else np.nan,
        "max": np.nanmax(temp_array) if len(temp_array) > 0 else np.nan,
    }


# Test with good and bad data
good_temps = [15.2, 16.1, 14.8, 15.9, 16.3]
bad_temps = [15.2, 150.0, 14.8, np.nan, 16.3]  # One outlier, one NaN

print("Validation of good data:")
result = validate_temperature_data(good_temps)
print(f"  Valid: {result['valid']}")
print(f"  Range: {result['min']:.1f} - {result['max']:.1f}°C")
print(f"  Mean: {result['mean']:.1f} ± {result['std']:.1f}°C")

print("\nValidation of bad data:")
result = validate_temperature_data(bad_temps)
print(f"  Valid: {result['valid']}")
print(f"  NaN values: {result['n_nan']}")
print(f"  Out of range: {result['n_above_max']}")

# %% [markdown]
# **2. Consistency Checks**


# %%
def validate_data_consistency(data_dict):
    """Check that all arrays have consistent lengths.

    Important for ensuring aligned time series or spatial data.
    """
    lengths = {key: len(val) for key, val in data_dict.items()}
    unique_lengths = set(lengths.values())

    if len(unique_lengths) == 1:
        return True, f"All arrays have length {unique_lengths.pop()}"
    else:
        return False, f"Inconsistent lengths: {lengths}"


# Example
data_good = {
    "time": [0, 1, 2, 3, 4],
    "temperature": [15.2, 16.1, 14.8, 15.9, 16.3],
    "pressure": [1013, 1012, 1014, 1013, 1012],
}

data_bad = {
    "time": [0, 1, 2, 3],  # Missing one point!
    "temperature": [15.2, 16.1, 14.8, 15.9, 16.3],
    "pressure": [1013, 1012, 1014, 1013, 1012],
}

valid, msg = validate_data_consistency(data_good)
print(f"Good data: {valid} - {msg}")

valid, msg = validate_data_consistency(data_bad)
print(f"Bad data: {valid} - {msg}")

# %% [markdown]
# **3. Metadata Validation**


# %%
def validate_fair_metadata(metadata):
    """Check that essential FAIR metadata is present."""
    required_fields = ["title", "creator", "created", "license"]
    recommended_fields = ["description", "keywords", "identifier"]

    missing_required = [f for f in required_fields if f not in metadata]
    missing_recommended = [f for f in recommended_fields if f not in metadata]

    issues = []
    if missing_required:
        issues.append(f"Missing required fields: {missing_required}")
    if missing_recommended:
        issues.append(f"Missing recommended fields: {missing_recommended}")

    valid = len(missing_required) == 0

    # Calculate completeness score
    total_fields = len(required_fields + recommended_fields)
    missing_fields = len(missing_required) + len(missing_recommended)
    completeness = (total_fields - missing_fields) / total_fields

    return {"valid": valid, "issues": issues, "completeness": completeness}


# Example
metadata_complete = {
    "title": "Temperature Dataset",
    "creator": "Dr. Smith",
    "created": "2026-02-10",
    "license": "CC-BY-4.0",
    "description": "Daily measurements",
    "keywords": ["temperature", "climate"],
    "identifier": "10.5281/zenodo.12345",
}

metadata_incomplete = {"title": "Temperature Dataset", "creator": "Dr. Smith"}

result = validate_fair_metadata(metadata_complete)
print(f"Complete metadata: Valid={result['valid']}, Completeness={result['completeness']:.0%}")

result = validate_fair_metadata(metadata_incomplete)
print(f"Incomplete metadata: Valid={result['valid']}, Completeness={result['completeness']:.0%}")
if result["issues"]:
    for issue in result["issues"]:
        print(f"  - {issue}")

# %% [markdown]
# ### Best Practices for Data Quality
#
# 1. **Validate early** - Check data as soon as it's collected
# 2. **Automate checks** - Build validation into your pipeline
# 3. **Document assumptions** - What ranges are "normal"?
# 4. **Keep raw data** - Never overwrite original measurements
# 5. **Log issues** - Record when and why data was flagged/corrected
# 6. **Version control for data** - Use git-annex, DVC, or similar
# 7. **Checksums** - Verify data integrity (MD5, SHA256)

# %% [markdown]
# ## Part 7: Best Practices and Recommendations
#
# ### The FAIR Data Checklist for Research Software
#
# **Before starting your project:**
# - [ ] Choose appropriate file formats for your data types
# - [ ] Plan metadata schema (what information to capture)
# - [ ] Decide on naming conventions
# - [ ] Set up backup system (3-2-1 rule)
# - [ ] Consider where to deposit data (institutional repo, Zenodo, domain-specific)
#
# **While collecting/generating data:**
# - [ ] Embed metadata with data (don't keep separate files)
# - [ ] Use standard vocabularies and units
# - [ ] Validate data continuously
# - [ ] Version control your data processing scripts
# - [ ] Document any data transformations
# - [ ] Keep raw data immutable
#
# **When publishing:**
# - [ ] Deposit data in appropriate repository
# - [ ] Get persistent identifier (DOI)
# - [ ] Choose appropriate license (CC-BY, CC0, etc.)
# - [ ] Link data to publication
# - [ ] Include comprehensive README
# - [ ] Provide example code for reading data
# - [ ] Archive exact software version used (containerize if possible)
#
# ### Format Recommendations by Field
#
# **Climate Science**: NetCDF with CF conventions
# **Genomics**: FASTQ, BAM/SAM, HDF5 for matrices
# **Astronomy**: FITS (Flexible Image Transport System)
# **Medical Imaging**: DICOM, NIfTI
# **Microscopy**: OME-TIFF (Open Microscopy Environment)
# **Geospatial**: GeoTIFF, Shapefile, GeoJSON
# **General tabular**: CSV for small, Parquet for large
# **General arrays**: HDF5
# **Time series**: HDF5, InfluxDB, or domain-specific
# **Relational**: SQLite for portable, PostgreSQL for server
#
# ### Common Pitfalls to Avoid
#
# **❌ Proprietary formats without converters**
# - Excel for large datasets (use CSV/Parquet)
# - MATLAB .mat files without documentation
# - Vendor-specific formats without open readers
#
# **❌ No metadata**
# - "The data is in column B" - which units? which instrument?
# - Separate metadata files that get lost
# - Assuming future-you will remember details
#
# **❌ Non-standard organization**
# - Random file naming (data1.txt, new_data_final_v3.txt)
# - No documentation of relationships between files
# - Mixed raw and processed data
#
# **❌ No validation**
# - Assuming data is correct
# - Not checking for missing values
# - Ignoring outliers
#
# **❌ Poor archival planning**
# - Only one copy on external drive
# - Formats that won't exist in 10 years
# - No migration plan
#
# ### What's Next?
#
# In **Lecture 12**, we'll explore scientific workflows and automation. You'll learn:
# - When to move beyond simple scripts to workflow management systems
# - Using Make for dependency-based execution
# - Writing Snakemake workflows for complex data analysis pipelines
# - Understanding alternatives like Nextflow and Common Workflow Language (CWL)
# - Integrating workflows with version control and containers
#
# The data management skills you've learned here become even more powerful when combined
# with automated workflows that process and analyze your data reproducibly.
#
# **Ready to continue? Move on to Lecture 12: Scientific Workflows and Automation!**
#
# ### Resources for Further Learning
#
# **FAIR Data:**
# - GO FAIR Initiative: https://www.go-fair.org/
# - FORCE11 FAIR Principles: https://www.force11.org/group/fairgroup/fairprinciples
# - RDA FAIR Data Maturity Model: https://www.rd-alliance.org/group/fair-data-maturity-model-wg
#
# **File Formats:**
# - HDF5 Documentation: https://www.hdfgroup.org/solutions/hdf5/
# - NetCDF User Guide: https://www.unidata.ucar.edu/software/netcdf/docs/
# - CF Conventions: http://cfconventions.org/
#
# **Data Repositories:**
# - Zenodo (general): https://zenodo.org/
# - Figshare (general): https://figshare.com/
# - Dryad (biological/medical): https://datadryad.org/
# - Domain-specific: Ask your librarian or data manager
#
# **Tools:**
# - Pandas: Tabular data manipulation
# - Xarray: Labeled multi-dimensional arrays (built on NumPy, works with NetCDF)
# - PyTables: Advanced HDF5 interface
# - DVC (Data Version Control): Git for data
# - Great Expectations: Data quality framework
#
# **Other Languages:**
# The concepts and file formats discussed here are language-agnostic.
# Libraries exist for HDF5, NetCDF, and SQLite in virtually all scientific
# computing languages. The FAIR principles apply regardless of implementation language.

# %% [markdown]
# ## Summary
#
# **Key Takeaways:**
#
# 1. **FAIR principles** guide how we manage research data for maximum impact
# 2. **Choose formats wisely** - consider longevity, interoperability, and community standards
# 3. **HDF5** is excellent for large hierarchical scientific data
# 4. **NetCDF** is the standard for climate/ocean/atmosphere data
# 5. **SQLite** is perfect for structured relational research data
# 6. **Metadata is not optional** - embed it with your data
# 7. **Validate early and often** - bad data leads to bad science
# 8. **Think long-term** - plan for data reuse 10+ years from now
#
# **The connection to Research Software Engineering:**
# - Good RSE practices enable FAIR data
# - Your software should write FAIR-compliant data files
# - Document your data formats as thoroughly as your code
# - Version control applies to data schemas too
# - Reproducibility requires both code AND data to be FAIR
#
# **Your action items:**
# 1. Review your current projects - are they FAIR compliant?
# 2. Choose appropriate file formats for your data
# 3. Add comprehensive metadata to existing datasets
# 4. Implement data validation in your pipelines
# 5. Plan for long-term preservation
#
# Remember: **Research data is a research output**. Treat it with the same care
# as your publications. Future researchers (including future you!) will thank you.
#
# ## References
#
# - Wilkinson et al. (2016). "The FAIR Guiding Principles for scientific data
#   management and stewardship". Scientific Data, 3:160018.
#   DOI: 10.1038/sdata.2016.18
#
# - Barker et al. (2022). "Introducing the FAIR Principles for research software".
#   Scientific Data, 9:622. DOI: 10.1038/s41597-022-01710-x
#
# - HDF Group. "HDF5 Documentation". https://www.hdfgroup.org/
#
# - Unidata. "NetCDF Documentation". https://www.unidata.ucar.edu/software/netcdf/
#
# - RDA FAIR Data Maturity Model Working Group. "FAIR Data Maturity Model".
#   DOI: 10.15497/RDA00050

# %%
