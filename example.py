from red_fileops.scan import ScanTarget, ScanResults, ScanEntity, Scanner
from red_fileops.sysinfo import PLATFORM

EX_SCAN_PATH: str = "/home/jack/mambaforge"

if __name__ == "__main__":
    print(f"Platform: {PLATFORM.platform_aliased}")
    
    SCANNER: Scanner = Scanner(scan_path=EX_SCAN_PATH)
    SCANNER.scan()

    if not SCANNER.scan_results:
        print(f"Scan results empty. Exiting.")
        
        exit(1)

    print(
        f"Scanner counts: [{SCANNER.scan_results.count_dirs}] dir(s) / [{SCANNER.scan_results.count_files}] file(s)"
    )

    _sample = SCANNER.scan_results.files[0]
    print(f"SAMPLE ({type(_sample)}): {_sample}")

    SCANNER.save_to_json()
    
    for p in SCANNER.scan_results.files[0:5]:
        entity: ScanEntity = ScanEntity(path=p.path)
        print(f"Scan result entity: {entity}")
        print(f"Created at: {entity.created_at}")
