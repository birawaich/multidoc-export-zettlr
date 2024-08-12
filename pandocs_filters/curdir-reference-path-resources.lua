-- filter to add the relative path from the current directory to the image
-- same as "mod-reference-path-resources" but useses other path!

local prefix = "" --default path prefix

function Meta(meta)
  if meta.resource_path_mod_curdir then
    prefix = pandoc.utils.stringify(meta.resource_path_mod_curdir)
    -- print("%Prefix set to: " .. prefix) -- Debug output
  end
end

function Image(elem)
    -- Modify the src attribute to use an absolute path
    -- lua regex matches to filename
    --print("%prefix is: "..prefix)
    elem.src = prefix .. "/" .. elem.src:match("([^/]+)$")
    return elem
end

--speficy order cf. https://pandoc.org/lua-filters.html --> Typewise Traversal
return {
    { Meta = Meta },  -- (1)
    { Image = Image }     -- (2)
}