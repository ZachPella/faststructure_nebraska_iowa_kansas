# FastStructure Analysis Tools

**Improved Python scripts for FastStructure output analysis and visualization**
<img width="1018" height="754" alt="Screenshot 2025-10-21 141107" src="https://github.com/user-attachments/assets/1075ce1e-8c4c-45e3-bec1-88ce9567eb2d" />
<img width="1812" height="461" alt="image" src="https://github.com/user-attachments/assets/5c4a3c55-c190-4bd5-ac27-8d3ad37ce6a0" />

## Why This Exists

FastStructure is a powerful tool for inferring population structure, but its official repository hasn't been updated in years. The original utility scripts have several critical issues that make them frustrating to use in modern workflows:

- **Parsing bugs** that cause silent failures or mismatched K values
- **Python 2 dependencies** that break in Python 3 environments
- **Basic plotting** with no customization for real-world data grouping
- **Poor error handling** that makes debugging a nightmare

Someone needed to fix this. So I did.

## What's Fixed & Improved

### 🔧 `chooseK.py` - Robust Model Selection

**Original Issues:**
- Fragile regex parsing that silently failed
- Array length mismatches between K values and likelihoods
- No validation of extracted data
- Cryptic failures with no useful error messages

**My Improvements:**
- ✅ **Bulletproof parsing** - extracts FINAL converged marginal likelihood values only
- ✅ **Comprehensive error handling** - warns about missing/malformed files
- ✅ **Array validation** - ensures K values match likelihood extractions
- ✅ **Python 2/3 compatibility** - works in both environments
- ✅ **Safe file handling** - uses context managers (`with` statements)
- ✅ **Removed external dependencies** - no more mysterious `vars.utils` imports

**Usage:**
```bash
python chooseK.py --input=faststructure_K
```

**Output:**
```
Model complexity that maximizes marginal likelihood = 5
Model components used to explain structure in data (modal bestK) = 4
```

---

### 📊 `extract_metrics.py` - Compile Analysis Data

**What It Does:**
This script wasn't in the original FastStructure toolkit. I created it to systematically extract and compile metrics across all K values for easy downstream analysis and plotting.

**Features:**
- Loops through K=1 to K=10 (or any range you specify)
- Extracts LLBO (log-likelihood bound) and K_phi_star (effective components) for each K
- Outputs a clean CSV file ready for plotting or further analysis
- Robust error handling for missing files

**Usage:**
```bash
python extract_metrics.py
```

**Output:**
Creates `k_metrics_data.txt`:
```
K,LLBO_Value,K_Phi_Star
1,-512345.678900,1
2,-498765.432100,2
3,-487654.321000,3
...
```

---

### 🎨 `plot.py` - Beautiful, Publication-Ready Admixture Plots

**Original FastStructure plotting:**
- Generic bar plots with no grouping
- No geographic or hierarchical organization
- Basic matplotlib styling
- No customization options

**My Custom Plotting:**
- ✅ **Hierarchical grouping** - samples organized by State → County → Individual
- ✅ **Multi-level labels** - clear visual hierarchy (e.g., "Nebraska" spanning multiple counties)
- ✅ **Custom sorting** - intelligent ordering for comparative analysis
- ✅ **Visual separators** - bold lines between geographic groups
- ✅ **Flexible** - easily adaptable to your dataset's structure
- ✅ **High-quality output** - publication-ready PDFs

**Usage:**
```bash
python plot.py 5  # For K=5
```

**Key Features:**

1. **Geographic Organization:**
   - Samples grouped by location (Iowa → Nebraska Counties → Kansas)
   - Sub-groups for Nebraska counties (Thurston, Dodge, Douglas, Sarpy)
   - Easy to modify `GROUP_ORDER` for your dataset

2. **Multi-Layer Labels:**
   ```
   Iowa          Nebraska                    Kansas
                 Thurston Dodge Douglas Sarpy
   [====] [====] [====] [====] [====] [====]
   ```

3. **Automatic Validation:**
   - Checks that K value matches Q-matrix columns
   - Validates sample counts match label counts
   - Clear error messages when files are missing

**Customization Example:**
```python
# Modify GROUP_ORDER for your populations
GROUP_ORDER = [
    'Population1',
    'Population2_SubgroupA',
    'Population2_SubgroupB',
    'Population3',
]
```

---

## Requirements

**Python Packages:**
```bash
pip install numpy pandas matplotlib
```

**Compatible with:**
- Python 2.7 (chooseK.py, extract_metrics.py)
- Python 3.x (all scripts, recommended)

---

## Complete Workflow

```bash
# 1. Run FastStructure for multiple K values
for K in {1..10}; do
    structure.py -K $K --input=mydata --output=faststructure_K$K
done

# 2. Choose optimal K
python chooseK.py --input=faststructure_K

# 3. Extract all metrics for analysis
python extract_metrics.py

# 4. Generate admixture plots for chosen K values
python plot.py 3
python plot.py 5
python plot.py 7
```

---

## File Structure Expected

```
your_project/
├── faststructure_K1.1.log
├── faststructure_K1.1.meanQ
├── faststructure_K2.2.log
├── faststructure_K2.2.meanQ
├── ...
├── name_and_state_county.txt  # Sample labels (for plotting)
└── scripts/
    ├── chooseK.py
    ├── extract_metrics.py
    └── plot.py
```

**Label File Format (one per sample):**
```
Sample1_Iowa
Sample2_Nebraska_Douglas
Sample3_Kansas
...
```

---

## Why You Should Use This

**If you're working with FastStructure and:**
- The original scripts are crashing or giving weird results
- You need to group samples by geography/population
- You want publication-quality figures
- You're tired of Python 2 compatibility issues
- You need better error messages to debug your data

**Then these scripts will save you hours of frustration.**

---

## Contributing

Found a bug? Have a dataset with different structure? Want to add features?

These scripts are designed to be readable and modifiable. The grouping logic in `plot.py` is clearly commented and easy to adapt to your specific needs.

---

## License

Use freely. Improve freely. FastStructure deserves better tools, and science should be reproducible.

---

## Acknowledgments

Built on FastStructure by Anil Raj, Matthew Stephens, and Jonathan K. Pritchard.

Their software is brilliant. Their Python scripts just needed some love.

---

**TL;DR:** FastStructure's GitHub hasn't been updated since the Obama administration. I fixed the broken scripts and made them actually useful for real research. You're welcome.
