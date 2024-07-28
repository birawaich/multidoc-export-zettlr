-- make_text_red.lua

-- Function to handle Str elements (plain text)
function Str(el)
    -- Wrap the text with LaTeX command for red text
    el.text = "\\textcolor{red}{" .. el.text .. "}"
    return el
  end