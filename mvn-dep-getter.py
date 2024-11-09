#!/usr/bin/env python3

import sys
import os
import subprocess
import xml.etree.ElementTree as ET
import shutil
import tempfile

def create_temp_pom(dependencies):
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

    dependenciesXML = ET.SubElement(project, "dependencies")
    for dep in dependencies:
        dependency = ET.SubElement(dependenciesXML, "dependency")
        ET.SubElement(dependency, "groupId").text = dep["dependency"]["group"]
        ET.SubElement(dependency, "artifactId").text = dep["dependency"]["artifact"]
        ET.SubElement(dependency, "version").text = dep["dependency"]["version"]

    pom_path = tempfile.mktemp(suffix="pom.xml")
    tree = ET.ElementTree(project)
    tree.write(pom_path, encoding="utf-8", xml_declaration=True)
    # Print the generated POM to stdout
    with open(pom_path, 'r', encoding='utf-8') as file:
        print(file.read())
        
    return pom_path

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <group:artifact:version>,<group:artifact:version>,... <output_directory>")
        sys.exit(1)

    gavs = sys.argv[1].split(",")
    output_directory = sys.argv[2]
    dependencies = []
    for gav in gavs:
        parts = gav.split(":")
        if len(parts) != 3:
            print(f"Invalid GAV format: {gav}. Use <group:artifact:version>")
            sys.exit(1)
        dependencies.append({ "dependency": { "group": parts[0], "artifact": parts[1], "version": parts[2] }})

    pom_path = create_temp_pom(dependencies)
    lib_dir = os.path.abspath(output_directory)

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
