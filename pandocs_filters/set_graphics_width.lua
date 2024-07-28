-- set_graphics_width.lua

-- Function to handle Image elements
function Image(el)
    -- Check if the format is LaTeX or if it is an image in a Markdown element

    -- Print debug information
    print("-- Image found with source: " .. (el.src or "nil"))

    print("Before modification: ")
    for k, v in pairs(el.attributes) do
        print(k, v)
    end

    if el.src then
      -- Modify the attributes to set width to \columnwidth
      el.attributes['width'] = '\\columnwidth'
      el.attributes['height'] = '10px'
    end


    print("After modification: ")
    for k, v in pairs(el.attributes) do
        print(k, v)
    end


    -- Return the (possibly modified) element
    return el
  end