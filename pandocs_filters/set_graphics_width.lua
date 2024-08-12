-- set_graphics_width.lua
-- reads the file size of the file in pixel and writes it to the element
-- !needs to run AFTER the right paths for the images have been made!

local function get_image_size(filename)
    -- Use ImageMagick's identify command to get the image dimensions in pixels
    local handle = io.popen('identify -format "%wx%h" "' .. filename .. '"')
    local result = handle:read("*a")
    handle:close()
    return result:match("(%d+)x(%d+)")
end

  
function Image(elem)
    -- Get the width and height in pixels
    local width, height = get_image_size(elem.src)
    -- if width then
    --     print("%Width="..width)
    -- end
    -- if height then
    --     print("%Height="..height)
    -- end
    if width and height then
        -- Set the width and height attributes in pixels
        elem.attributes['width'] = width .. 'px'
        elem.attributes['height'] = height .. 'px'
    end
    return elem
end