from red_fileops import ScanTarget, ScanResults, ScanEntity

if __name__ == "__main__":
    SCANNER = ScanTarget(path="D:/Data/Downloads")
    results: ScanResults = SCANNER.scan()
    print(
        f"Results ({type(results)}) | Dirs: {results.count_dirs}, Files: {results.count_files}"
    )

    SCANNER.save_to_json()

    for p in results.files[0:5]:
        entity: ScanEntity = ScanEntity(path=p.path)
        print(f"Scan result entity: {entity}")
        print(f"Created at: {entity.created_at}")
