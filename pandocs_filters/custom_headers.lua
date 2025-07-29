-- Map Pandoc header levels to custom LaTeX commands
local header_map = {
  [1] = "mezdocsection",
  [2] = "mezdocsubsection",
  [3] = "mezdocsubsubsection",
  [4] = "mezdocparagraph",
  [5] = "mezdocsubparagraph",
  [6] = "mezdoclevelsix",
}

function Header(el)
  local cmd = header_map[el.level]
  if cmd then
    -- Generate LaTeX command manually
    local content = pandoc.utils.stringify(el.content)
    return pandoc.RawBlock("latex", "\\" .. cmd .. "{" .. content .. "}")
  else
    return el  -- fallback: leave unchanged
  end
end