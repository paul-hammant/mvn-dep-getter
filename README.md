# Maven Dependency Getter

This script is designed to fetch Maven dependencies for specified GAV (Group, Artifact, Version) coordinates and copy them into a local `lib` directory.

## Prerequisites

- Python 3.x
- Maven installed and configured in your system's PATH

## Usage

To run the script, use the following command:

```bash
python3 mvn-dep-getter.py <group:artifact:version>,<group:artifact:version>,... <output_directory>
```

### Example

```bash
python3 mvn-dep-getter.py org.forgerock.cuppa:cuppa:1.7.0,org.example:example-artifact:1.0.0 lib
```

### example set

`org.forgerock.cuppa:cuppa:1.7.0,org.hamcrest:hamcrest:3.0,com.squareup.okhttp3:okhttp:5.0.0-alpha.14,org.mockito:mockito-core:5.14.2`

This will generate a temporary POM file, resolve the specified dependencies, and copy them to the `lib` directory.

## Running via Curl

You can also run the script directly from a GitHub raw endpoint using `curl` and `python3`. Replace `https://example.com/mvn_deps.py` with the actual URL of the raw script.

```bash
curl -s https://example.com/mvn_deps.py | python3 - <group:artifact:version>,<group:artifact:version>,... <output_directory>
```

### Example

```bash
curl -s https://example.com/mvn_deps.py | python3 - org.forgerock.cuppa:cuppa:1.7.0,org.example:example-artifact:1.0.0 lib
```

This will execute the script directly from the URL, generating a temporary POM file, resolving the specified dependencies, and copying them to the `lib` directory.

1. The script takes a comma-separated list of GAVs as input.
2. It generates a temporary POM file with the specified dependencies.
3. It uses Maven to resolve and download the dependencies.
4. The dependencies are copied to the `lib` directory.

## Cleaning Up

The temporary POM file is automatically deleted after the dependencies are copied.

## License

This project is licensed under the MIT License.
