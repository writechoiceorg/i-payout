import os
import yaml


def read_yml_files(folder_path):
    paths_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".yml"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                yml_content = yaml.safe_load(file)
                if "paths" in yml_content:
                    for path in yml_content["paths"]:
                        version = extract_version(path)
                        cleaned_path = path.replace(f"/api/v{version}/", "")
                        paths_dict[path] = (
                            f'openAPI/{filename}#/paths/{cleaned_path.replace("/", "~1")}'
                        )
    return paths_dict


def extract_version(path):
    # Assumes the version is part of the path like /api/v{version}/...
    parts = path.split("/")
    for part in parts:
        if part.startswith("v") and part[1:].isdigit():
            return part[1:]  # Remove 'v' and return the version number
    return "unknown"  # Default value if version is not found


def write_new_yml_file(output_path, paths_dict):
    new_yml_content = {"paths": {}}
    for path, ref in paths_dict.items():
        new_yml_content["paths"][path] = {"$ref": ref}

    with open(output_path, "w") as file:
        yaml.dump(new_yml_content, file, default_flow_style=False)


def main():
    folder_path = "openAPI"  # Folder containing .yml files
    output_path = "output.yml"  # Output .yml file

    paths_dict = read_yml_files(folder_path)
    write_new_yml_file(output_path, paths_dict)
    print(f"New YML file generated at {output_path}")


if __name__ == "__main__":
    main()
