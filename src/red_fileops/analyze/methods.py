from red_fileops.scan import Scanner, ScanEntity, ScanResults, ScanTarget

import pandas as pd

def analyze_scan_results(scanner_obj: Scanner = None):
    assert scanner_obj is not None, ValueError("scanner should not be None")
    if scanner_obj.target is None:
        target: ScanTarget = ScanTarget(path=scanner_obj.scan_path)
        scanner_obj.target = target

    if scanner_obj.scan_results is None:
        print(f"[WARNING] Scan results are empty, initiating scan now")
        scanner_obj.scan()
        
    print(f"Scan results: [{len(scanner_obj.scan_results.dirs)}] dir(s), [{len(scanner_obj.scan_results.files)}] file(s)")
    
    entity_dicts: list[dict] = []
    
    for f in scanner_obj.scan_results.files:
        f_dict = f.model_dump()
        entity_dicts.append(f_dict)
    for d in scanner_obj.scan_results.dirs:
        d_dict = d.model_dump()
        entity_dicts.append(d_dict)
        
    print(f"Sample dict ({type(entity_dicts[0])}): {entity_dicts[0]}")
    
    try:
        entities_df: pd.DataFrame = pd.DataFrame.from_dict(entity_dicts, orient='columns')
    except Exception as exc:
        msg = Exception(f"Unhandled exception converting ScanEntity objects to DataFrame. Details: {exc}")
        print(f"[ERROR] {msg}")
        
        raise msg
    
    if entities_df is None or isinstance(entities_df, pd.DataFrame) and entities_df.empty:
        print(f"No entities found in scan results.")
        
        return None

    print(f"Entity DF shape: {entities_df.shape[0]}")
    print(entities_df.head(5))
    