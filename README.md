# Implementing and Evaluating Bernstein Bounds for Caustics - DH2323 Project

This project reproduces and analyzes the paper "Bernstein Bounds for Caustics".（[https://zhiminfan.work/paper/bound_caustics_preprint.pdf](https://zhiminfan.work/paper/bound_caustics_preprint.pdf)）
Based on the Mitsuba 0.6 framework, it implements the two-stage pipeline of precomputation and rendering.

**Full Report** (link to be added)

---

## Abstract

The Bernstein bounds-based caustics rendering algorithm is a deterministic sampling approach designed for accurate simulation of high-frequency lighting phenomena. By leveraging the bounding properties of Bernstein polynomials, the method precomputes conservative position and irradiance bounds for triangle tuples during the precomputation phase to effectively guide bound-driven triangle sampling during rendering. This report reproduces and analyzes this algorithm within the Mitsuba 0.6 framework. I validate the physical correctness of the algorithm across reflection and refraction scenes, focusing on the joint effects of sampling parameters (samples per pixel, the sampling probability factor 𝛾, and distribution cutoff) and material surface roughness (Alpha) on noise reduction and caustic profiles. Experimental results demonstrate that increasing spp is the most effective means of noise reduction, whereas modulating 𝛾 yields limited variance reduction in this setups. Additionally, the algorithm correctly responds to roughness variations, establishing a foundation for future caustic-driven visual perception studies.

---

## Repository Structure
```text
bound-caustics/
├── mts1/                        # Mitsuba 0.6 core engine & C++ integrator plugin
│   └── src/integrators/         # Core implementation of path_cuts_path integrator
│       └── mbglints/            # Runtime: distr.h, glintbounce.h (Sampling & Newton solvers)
├── bounder/                     # Single-scattering: C++ real-time bounding logic when loading .obj
├── batch/                       # Python precomputation scripts (for double-scattering scenes)
│   ├── alias.py                 # Scene configuration parameters
│   ├── run_mesh.py              # Generates spatial distribution file: results/sample_map.txt
│   └── bounder.py               # Main pipeline for position/irradiance bounding
└── test/                        # Test scenes & evaluation configurations
│   ├── fig_plane/               # Single reflection (conductor) setup
│   ├── fig_sphere/              # Single refraction (dielectric) setup
│   ├── fig_slab/                # Double refraction
│   └── fig_diamond/             # Multi-faceted high-frequency topology
├── 2d/                          # 2D demo (Bernstein polynomial visualization)
└── data/                        # scene OBJ files
```

**Note**: `results/sample_map.txt` is the precomputed caustic distribution data. It is generated locally at runtime and not pushed to the repository.

---

## Build

The rendering backend is based on https://github.com/VicentChen/mitsuba. Please install the dependency first, and set the correct dependency paths and Python 3.9 path in `mts1/CMakeLists.txt`. 

Python environment: Python 3.9 with numpy, scipy, numba, matplotlib, tqdm.

```bash
cd mts1
mkdir cbuild
cd cbuild
cmake ..
```
Then build the generated project in cbuild. Tested on Windows 10, Visual Studio 2022. The implementation builds upon Mbglints and CyPolynomials.

## Reproduce

- **Fig.1 Single reflection (Plane).** Please run `test/fig_plane/test.py`.  

- **Fig.2 Single refraction (Sphere).** Please run `test/fig_sphere/test.py`.  

- **Fig.4 Double refraction (Slab).** Modify `batch/alias.py` according to `test/fig_slab/alias.md` and then run `batch/run_mesh.py` to generate the distribution file. Finaly, run `test/fig_slab/test.py`.

- **Fig.5 Double refraction (Diamond).** Modify `batch/alias.py` according to `test/fig_diamond/alias.md` and then run `batch/run_mesh.py` to generate the distribution file. Finaly, run `test/fig_diamond/test.py`.
  
All rendered images in the report can be found as .exr files in `test/fig_*/results/`.


## Process and Updates

### 2025 May

#### 5.1 Build and Setup

Completed `mts1/cbuild` Release build.

#### 5.6 Single Scattering Debugging

Single reflection and single refraction run directly. However, the initial Sphere render was too bright, with caustics completely overexposed.
<img width="1920" height="1080" alt="fig_sphere_Bounded_intensity50" src="https://github.com/user-attachments/assets/5c0c282a-54ce-496e-8003-d632e0980b0a" />

Root cause: light intensity was set to 50. After reducing it to 10, the caustic brightness returned to normal and the refraction details became clear.
<img width="1920" height="1080" alt="fig_sphere_Bounded_intensity10_intIOR 1 5" src="https://github.com/user-attachments/assets/bf221556-1569-43ad-b4a9-d13571560faf" />

#### 5.7 Double Scattering: Missing Caustics

The Slab scene rendered with no caustic pattern on the ground.
<img width="1920" height="1080" alt="fig_slab_Bounded_no" src="https://github.com/user-attachments/assets/2e254ef1-6489-4f7b-89e0-1244db954a03" />


Debugging steps:

1. Checked scene files: objects were missing `caustic_caster_multi` and `caustic_bouncer` flags; the ground was missing `caustic_receiver`. Adding them did not help.

2. Found mismatch between precomputed data and rendering parameters: `alias.py` used light position `(1,2,-2)`, but the renderer defaulted to `(3,1,4)`. After fixing XML parameter passing, caustics still did not appear.
- At the same time, I can further confirm that the light source position should be (1, 2, -2); the renderer’s default settings are likely remnants from the original author’s rendering of the
diamond scene.
<img width="1920" height="1080" alt="fig_slab_Bounded_ChangeLightPosition" src="https://github.com/user-attachments/assets/1f761de2-d373-4028-bbea-94151be67b8c" />


3. Tried SPPM on the same scene, still no caustics. Python geometry validation showed that about 3850 refraction paths could land on the ground within `[0,1]`, confirming the scene geometry itself was fine.

The root cause was finally identified: the `COMPACT_MEMORY` macro in `distr.h` incorrectly degraded the double refraction triangle pair `(ti, tj)` to `(ti, ti)`, causing the Newton solver to find no valid paths.

After commenting out `#define COMPACT_MEMORY` and recompiling, the log showed non-empty queries increased from 0 to about 1.3 million, and caustics finally appeared correctly.
<img width="1920" height="1080" alt="fig_slab_Bounded" src="https://github.com/user-attachments/assets/89f689a8-88a5-4bea-b31e-c4d20f4ed857" />


#### 5.11 Diamond: parameters fix and Noise Reduction

Initial renders had no caustics. After adjustments based on Slab experience, caustics appeared but diamond facets had no reflections, and colors differed from the reference paper.
<img width="1920" height="1080" alt="fig_diamond_Bounded_single light source" src="https://github.com/user-attachments/assets/a4c31816-6eff-4a65-9191-17beb4979c74" />


Investigation showed that `diamond_pcp.xml` did not pass parameters (light position, `CHAIN_TYPE=22`, `SHADING_NORMAL`, `U1T`) to the integrator, so the renderer used defaults (single reflection, wrong light). After fixing parameter passing and regenerating the distribution file, caustics rendered successfully.(spp=1)
<img width="1920" height="1080" alt="fig_diamond_Bounded1_spp1" src="https://github.com/user-attachments/assets/c9d5e030-8185-4ec4-acb1-5d761f83bd41" />


Diamond has much higher noise than Slab because light bounces many times inside the faceted geometry. Several sampling configurations were tested:

| Config | spp | gamma/other | Result |
|--------|-----|-------------|--------|
| `cs_gamma10` | 3 | `gamma=10` | noisy |
| `cs_one` | 6 | `force_sample=1` | still noisy |
| `cs_one` + higher spp | 32 | `force_sample=1` | clean convergence |

<img width="2105" height="747" alt="Fig 7" src="https://github.com/user-attachments/assets/351d784c-d7cf-4337-8286-d9682aca9f67" />

Conclusion: adjusting `gamma` and `force_sample` helps little; **increasing spp is the most effective way to reduce noise**. At `spp=32`, render time increased from 44s to about 4 minutes, but the caustic fire became clean and converged.
<img width="1920" height="1080" alt="fig_diamond_cs_one_spp32" src="https://github.com/user-attachments/assets/8f7f13ae-83af-4385-a77e-121d56e5bcb8" />


#### 5.12-5.13 Effect of Roughness (alpha) on Caustics

**Reflection scene**: Changed `conductor` to `roughconductor` and tested `alpha = 0.05, 0.2`. Larger `alpha` produces wider and fainter caustics.
<img width="3028" height="825" alt="Fig  9" src="https://github.com/user-attachments/assets/33b7f1e8-2726-42c8-b2d0-a81d1dccc2fc" />

**Refraction scene**: Modifying IOR caused the sphere to become dark, because with only a single light source, refracted rays bent away from the camera. Switched to using `alpha` instead. Changed `dielectric` to `roughdielectric` and tested `alpha = 0.05, 0.1, 0.3`. `alpha` affects both object appearance (whiter, cloudier) and caustic shape (wider, fainter).
<img width="1411" height="842" alt="微信图片_20260522181928_507_108" src="https://github.com/user-attachments/assets/d657b5a7-94c3-4333-8c96-e45df634eb87" />


#### 5.14 Mitsuba Crash from Debug/Release Mixing

After finishing double scattering debugging, I returned to the plane scene to test rendering times with different `spp` values. Mitsuba reported an error:

> `mitsuba-core.dll` failed to load `boost_thread-vc142-mt-x64-1_77.dll`

To investigate, I compiled a Debug version of the plugin. The Debug version loaded `boost_thread-vc142-mt-gd-x64-1_77.dll` successfully, so I continued debugging with Debug builds.

The problem: CMake outputs both Debug and Release builds to `mts1/cbuild/bin`. During debugging, I compiled Debug versions of `mitsuba.exe`, `mitsuba-core.dll`, `path_cuts_path.dll`, etc., which gradually overwrote the original Release files.

The root issue was mixing:

- Release `boost_thread-vc142-mt-x64-1_77.dll` could not be loaded by the loader
- Debug `boost_thread-vc142-mt-gd-x64-1_77.dll` could be loaded, but its ABI was incompatible with Release-compiled plugins

Trying to replace Release DLLs with renamed Debug DLLs:

- `mitsuba-core` started
- but `mitsuba-render.dll` failed to initialize (ABI/runtime mismatch)

A full Release rebuild still failed. Further investigation showed that newer MSVC versions add `volatile metadata` to DLLs by default, which the current environment loader could not recognize.

**Final solution**:

1. Rebuild Boost in the dependency directory
2. Copy the working Boost DLLs to the filenames expected by Mitsuba
3. Set environment variable `CL=/volatileMetadata-`
4. Perform a clean Release rebuild of Mitsuba (main program + `path_cuts_path` + scene plugins)

After this, the program ran normally again.

#### 5.18 Rendering Time and Timeout Mechanism

| Config | Time |
|--------|------|
| `spp=1, timeout=1` | very noisy (smoke test) |
| `spp=20, timeout=0` | 15.3s |
| `spp=40, timeout=0` | 30.7s |

<img width="1672" height="941" alt="Fig  8" src="https://github.com/user-attachments/assets/80958e56-3dcf-4494-aedc-21949020617a" />

Time scales linearly with `spp`. Setting `timeout` too small terminates incomplete iterative paths early, resulting in black blocks or hard noise. For high-quality rendering, `timeout=0` must be used.

#### 5.19 𝛾 and Distribution Flattening

In the Slab scene, `force_gamma=70` and `force_gamma=5000` showed almost no difference in noise. The parameter that caused a sharp noise increase was `distr_max=0.0001` — it flattened the distribution, causing the algorithm to degenerate into uniform sampling. For smooth scenes, adjusting `gamma` is ineffective; increasing `spp` is the right solution.
<img width="2071" height="759" alt="Fig  6" src="https://github.com/user-attachments/assets/f56c9a77-b20d-42ff-b552-f263f30462dd" />


---




## Acknowledgement

The source code is based on https://github.com/mollnn/bound-caustics.git. I sincerely thank the authors for kindly releasing their code and scenes, as well as for their great work.
