# New Language

## Organization

1. Create a directory in `/languages` with the name of your language

This directory should follow this structure:

```
bin
    deploy.sh
src
    bin
        build.sh
    extensions
        parameter-store-extension
    example
        src
            <YOUR LANGUAGE HANDLER FILES>
        deploy.sh
        README.md
    parameter-store-extension
        extension.<YOUR LANGUAGE EXTENSION>
    .gitignore
    README.md
```
