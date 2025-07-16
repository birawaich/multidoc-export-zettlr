# Multidoc Export for Zettlr

Multi Document Export for Zettlr Markdown Files.

Export multiple markdown documents made in [Zettlr](https://github.com/Zettlr/Zettlr) to a PDF. Intended to concatenate notes into one file for print. A Build Descriptor File specifies how which markdown file is added.

Status: In Development, adding things as I need/want them ;)
Intend: Private use, feel free to use if it is useful for you too!  

## Supported Features

See the sample files and generate them to see what Markdown features are supported.

## Build Descriptor Files

Build Descriptor Files are YAML files that describe how multiple files should be merged together. Information is given in the top level object. The files to be included can be nested hierarchy.

See `sample/build.yaml` for an example. The following list describes the different fields.

-   (Object) `BuildDescription`  
    Main object to represent one build. Has the following fields:
    -   `title`  
        (String) Title of the merged document.
    -   `author_name`  
        (String) Name of the Author to be printed.
    -   `author_email`  
        (String) E-mail of the Author to be printed and linked.
    -   `filepath_source`  
        (String) Filepath the single documents are relative to. Can be absolute or relative (to the build descriptor file).
    -   `filepath_destination`  
        (String) Filepath to the destination where the resulting LaTex and PDF files should lie. Can be absolute or relative (to the build descriptor file).
    -   `include`  
        (Array) of files (as relative paths --> String) to be included or Section Objects.
-   (Object) `Section`  
    Object of a section. Has the following fields:
    -   `title`  
        (String) Title of this Section.
    -   `content`  
        (Array) of files (as relative paths --> String) to be included or Section Objects.

## Implementation Details

### Handling of Images

Handling images is tricky due to different image locations as well as image height and width. The following is done:

(1) During the modification phase of the markdown files two extra meta fields is added to the YAML meta header of each single document:

-   `resource_path_mod`  
    The relative path from the output directory to the source directory.
-   `resource_path_mod_curdir`  
    The relative path from the current directory to the source directory.

(2) During the compilation to LaTex via Pandocs Lua filters are used to adjust different properties. Note that the order is important!

1.  `curdir-refeerence-path-resources.lua`  
    Modifies the source of all images to be `resource_path_mod_curdir`  (set in step 1) + the image filename. This is used by the next filter to find the height and width of the image.
2.  `set_graphics_width.lua`  
    Reads the width and height of the image with ImageMagick identify command and then sets the height and with of the image in pixels.
3.  `mod-reference-path-resources.lua`  
    Modifies the source of all images to be `resource_path_mod` (set in step 1) + the image filename. This is needed such that latex (that has as a working directory and thus reference the output path) can find the image.

(3) The raw LaTex output is then modified. During this modification the function `SingleDocument._add_width_to_includegraphics()` scales the attributes or sets them to the maximum of a column.

 ## To Do

-   Support Hierarchy
    Currently the hierarchy in the build descriptor file is ignored.
-   Support exporting online short summaries

-   Nice To Have
    -   Installation Guide (if anyone needs it incl. myself)
    -   Proper Licensing

