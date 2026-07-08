# distance.py — .python_packages/scipy/spatial/distance.py

## Tożsamość
- **id_karty:** `REPO-DISTANCE-B126`
- **ścieżka:** `.python_packages/scipy/spatial/distance.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.971`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/spatial/distance.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.971 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Distance computations (:mod:`scipy.spatial.distance`)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CDistMetricWrapper, PDistMetricWrapper, MetricInfo
- **funkcje:** `_copy_array_if_base_present`, `_correlation_cdist_wrap`, `_correlation_pdist_wrap`, `_convert_to_type`, `_nbool_correspond_all`, `_nbool_correspond_ft_tf`, `_validate_cdist_input`, `_validate_weight_with_size`, `_validate_hamming_kwargs`, `_validate_mahalanobis_kwargs`, `_validate_minkowski_kwargs`, `_validate_pdist_input`, `_validate_seuclidean_kwargs`, `_validate_vector`, `_validate_weights`, `directed_hausdorff`, `minkowski`, `euclidean`, `sqeuclidean`, `correlation`, `cosine`, `hamming`, `jaccard`, `seuclidean`, `cityblock`, `mahalanobis`, `chebyshev`, `braycurtis`, `canberra`, `jensenshannon`

## Opis
Distance computations (:mod:`scipy.spatial.distance`)
=====================================================

.. sectionauthor:: Damian Eads

Function reference
------------------

Distance matrix computation from a collection of raw observation vectors
stored in a rectangular array.

.. autosummary::
   :toctree: generated/

   pdist   -- pairwise distances between observation vectors.
   cdist
