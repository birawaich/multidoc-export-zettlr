-- Map Pandoc header levels to custom LaTeX commands
local header_map = {
  [1] = "mezdocsection",
  [2] = "mezdocsubsection",
  [3] = "mezdocsubsubsection",
  [4] = "mezdocparagraph",
  [5] = "mezdocsubparagraph",
  [6] = "mezdoclevelsix",
}
-- Escape LaTeX special characters in text
local function escape_latex(str)
  local replacements = {
    ["\\"] = "\\textbackslash{}",
    ["{"] = "\\{",
    ["}"] = "\\}",
    ["$"] = "\\$",
    ["&"] = "\\&",
    ["#"] = "\\#",
    ["%"] = "\\%",
    ["_"] = "\\_",
    ["^"] = "\\textasciicircum{}",
    ["~"] = "\\textasciitilde{}",
  }
  return (str:gsub(".", function(c)
    return replacements[c] or c
  end))
end
-- Manually convert inlines to LaTeX
local function inline_to_latex(inlines)
  local result = {}
  for _, inline in ipairs(inlines) do
    if inline.t == "Str" then
      table.insert(result, escape_latex(inline.text))
    elseif inline.t == "Space" then
      table.insert(result, " ")
    elseif inline.t == "Math" then
      local delim = inline.mathtype == "DisplayMath" and "$$" or "$"
      table.insert(result, delim .. inline.text .. delim)
    elseif inline.t == "Code" then
      table.insert(result, "\\texttt{" .. escape_latex(inline.text) .. "}")
    elseif inline.t == "Emph" then
      table.insert(result, "\\emph{" .. inline_to_latex(inline.c) .. "}")
    elseif inline.t == "Strong" then
      table.insert(result, "\\textbf{" .. inline_to_latex(inline.c) .. "}")
    elseif inline.t == "RawInline" and inline.format == "latex" then
      table.insert(result, inline.text)
    else
      -- fallback: escape stringified version
      table.insert(result, escape_latex(pandoc.utils.stringify(inline)))
    end
  end
  return table.concat(result)
end
-- actual function to go through headers
function Header(el)
  local cmd = header_map[el.level]
  if cmd then
    -- Generate LaTeX command manually
    local content = inline_to_latex(el.content)
    return pandoc.RawBlock("latex", "\\" .. cmd .. "{" .. content .. "}")
  else
    return el  -- fallback: leave unchanged
  end
end