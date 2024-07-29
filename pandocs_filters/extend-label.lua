-- UNTESTED from ChatGPT

local prefix = "default-"

function Meta(meta)
  if meta.heading_prefix then
    prefix = pandoc.utils.stringify(meta.heading_prefix)
  end
end

function Header(el)
  if el.identifier ~= "" then
    el.identifier = prefix .. el.identifier
  end
  return el
end