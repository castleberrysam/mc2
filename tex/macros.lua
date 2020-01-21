--[[
  Generates a diagram for bitfields in a register, data type, or data structure.
  The single arg is a comma separated list.
  A normal entry is two elements, the first is the field name and the second is the bit width.
  There are also directives, starting with !, to change the table formatting.

  !SEP:
  Inserts a visual break in the row, for grouping fields together into larger objects.

  !WIDTH <N>:
  Overrides the visual width to use in the diagram for the field immediately after the directive.
  Bit numbering will still use the original width.

  !ROW:
  Starts a new row in the diagram. The bit numbering for each row is done independently.
  All rows in the diagram must have the same visual width.
  The visual width of a field is the same as its bit width, except when the !WIDTH directive is used.

  !LBL <label>:
  Prints a label to the left of the diagram, aligned with the current row.
  Can be used either before or after the !ROW directive, but has to occur at the beginning of a row.
--]]
function insntbl(args)
  -- Parse comma separated arguments and directives
  local argt = {}
  local arg = {}
  local numcols = nil
  local rowlabel = nil
  local state = 0
  for tok in string.gmatch(args, "%s*([^,]*)%s*,") do
    if string.sub(tok, 1, 1) == "!" then
      if state ~= 0 then
        tex.error("Malformed arguments to insntbl")
      end
      if tok == "!SEP" then
        argt[#argt].separate = true
      elseif tok == "!ROW" then
        argt[#argt].endrow = true
      else
        m = string.match(tok, "!WIDTH%s+(%d+)")
        if m then
          numcols = m
        else
          m = string.match(tok, "!LBL%s+(.+)")
          if m then
            rowlabel = m
          else
            tex.error("Unknown or malformed directive to insntbl")
          end
        end
      end
    elseif state == 0 then
      arg.label = tok
      state = 1
    else
      arg.numbits = tok
      arg.numcols = numcols or arg.numbits
      arg.rowlabel = rowlabel
      table.insert(argt, arg)
      arg = {}
      numcols = nil
      rowlabel = nil
      state = 0
    end
  end
  argt[#argt].endrow = true

  -- Calculate indices
  local base = 0
  local width = 0
  local index = 0
  for i,arg in ipairs(argt) do
    if index == 0 then
      base = base + width
      width = _getwidth(argt, i, false)
      index = width
    end
    index = index - arg.numbits
    arg.index = base + index
    if arg.endrow then
      base = 0
      width = 0
    end
  end

  -- Calculate number of columns
  local newrow = false
  local haverowlabels = false
  local numcols = _getwidth(argt, 1, true)
  for i,arg in ipairs(argt) do
    if arg.rowlabel then
      haverowlabels = true
    elseif arg.endrow then
      newrow = true
    elseif newrow then
      if _getwidth(argt, i, true) ~= numcols then
        tex.error("Row length mismatch in insntbl")
      end
      newrow = false
    end
  end

  -- Write table start
  -- Column spec doesn't really matter since multicols will override it
  local ret = {}
  table.insert(ret, "\\gap{\\setlength{\\tabcolsep}{0pt}\\begin{tabular}{")
  if haverowlabels then
    table.insert(ret, "C")
  end
  table.insert(ret, string.rep("B{1}", numcols))
  table.insert(ret, "}")

  -- Precompute string to use for hlines
  if haverowlabels then
    hline = string.format("\\cline{2-%d}", numcols+1)
  else
    hline = "\\hline "
  end

  -- Write rows
  local rowstart = 1
  local state = 0
  local i = 1
  repeat
    arg = argt[i]

    -- Row start and delimiters
    if i == rowstart then
      table.insert(ret, hline)
      if haverowlabels then
        if arg.rowlabel and state == 0 then
          table.insert(ret, arg.rowlabel)
          table.insert(ret, "\\hspace*{6pt}")
        end
        table.insert(ret, "&")
      end
    else
      table.insert(ret, "&")
    end

    -- Row contents
    if state == 0 then
      str = string.format("\\multicolumn{%s}{%sB{%s}|%s}{%s}",
                          arg.numcols,
                          ((i == rowstart) and "|") or "",
                          arg.numcols,
                          (arg.separate and "|") or "",
                          arg.label)
    else
      str = string.format("\\multicolumn{%s}{R}{%s}", arg.numcols, arg.index)
    end
    table.insert(ret, str)

    -- Row terminator
    i = i + 1
    if arg.endrow then
      table.insert(ret, "\\\\")
      if state == 0 then
        i = rowstart
        state = 1
      else
        rowstart = i
        state = 0
      end
    end
  until i > #argt

  -- Terminate table and commit
  table.insert(ret, "\\end{tabular}}%")
  texsend(table.concat(ret))
end

-- Utility function used by insntbl
function _getwidth(argt, start, columns)
  local acc = 0
  for i = start, #argt do
    arg = argt[i]
    acc = acc + ((columns and arg.numcols) or arg.numbits)
    if (not columns and arg.separate) or arg.endrow then
      break
    end
  end
  return acc
end

-- Utility function for debugging
function texsend(str)
  --texio.write(str)
  tex.print(str)
end
