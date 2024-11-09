#!/usr/bin/env python3

import sys
import os
import subprocess
import xml.etree.ElementTree as ET
import shutil
import tempfile

def create_temp_pom(group_id, artifact_id, version):
    # Generate POM XML structure
    namespaces = {
        "xmlns": "http://maven.apache.org/POM/4.0.0",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
    }
    project = ET.Element("project", **namespaces)
    ET.SubElement(project, "modelVersion").text = "4.0.0"
    ET.SubElement(project, "groupId").text = "group_id"
    ET.SubElement(project, "artifactId").text = "artifact_id"
    ET.SubElement(project, "version").text = "version"

    dependencies = ET.SubElement(project, "dependencies")
    dependency = ET.SubElement(dependencies, "dependency")
    ET.SubElement(dependency, "groupId").text = group_id
    ET.SubElement(dependency, "artifactId").text = artifact_id
    ET.SubElement(dependency, "version").text = version

    pom_path = tempfile.mktemp(suffix="pom.xml")
    tree = ET.ElementTree(project)
    tree.write(pom_path, encoding="utf-8", xml_declaration=True)
    # Print the generated POM to stdout
    with open(pom_path, 'r', encoding='utf-8') as file:
        print(file.read())
        
    return pom_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <group:artifact:version>")
        sys.exit(1)

    gav = sys.argv[1].split(":")
    if len(gav) != 3:
        print("Invalid GAV format. Use <group:artifact:version>")
        sys.exit(1)

    group_id, artifact_id, version = gav
    pom_path = create_temp_pom(group_id, artifact_id, version)
    lib_dir = os.path.abspath("./lib")

    try:
        # Run mvn dependency:go-offline
        subprocess.run(["mvn", "-f", pom_path, "dependency:tree"], check=True)
        subprocess.run(["mvn", "-f", pom_path, "dependency:go-offline"], check=True)
        # Copy all jars to ./lib
        subprocess.run(["mvn", "-f", pom_path, "dependency:copy-dependencies", f"-DincludeTransitive=true", f"-DoutputDirectory={lib_dir}", "-DincludeScope=runtime"], check=True)
        print(f"Dependencies copied to {lib_dir}")
    finally:
        os.remove(pom_path)

if __name__ == "__main__":
    main()
