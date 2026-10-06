import React from 'react';

/**
 * Renders inline text with bolding (**text**) and citation badges ([1], [2]).
 */
function renderInline(text) {
  if (!text) return null;

  // Tokenize string by **bold** and [1] citation markers
  // Regex captures:
  // 1: bold text (between **)
  // 2: citation number (between [])
  const parts = [];
  const regex = /(\*\*([^*]+)\*\*|\[(\d+)\])/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    if (match[2] !== undefined) {
      // Bold match
      parts.push(
        <strong key={`b-${match.index}`} className="font-semibold text-slate-900">
          {match[2]}
        </strong>
      );
    } else if (match[3] !== undefined) {
      // Citation match [n]
      parts.push(
        <span
          key={`c-${match.index}`}
          className="inline-flex items-center justify-center px-1 py-0.2 mx-0.5 text-[10.5px] font-bold text-teal-700 bg-teal-50 border border-teal-200 rounded align-baseline shadow-2xs select-none"
          title={`Source Citation [${match[3]}]`}
        >
          [{match[3]}]
        </span>
      );
    }

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts;
}

/**
 * Parses markdown text blocks and renders structured, accessible HTML:
 * - Section headers (**Header:** or ### Header)
 * - Clean bullet lists (- item)
 * - Numbered lists (1. item)
 * - Grounded paragraphs with inline citations
 */
export default function FormattedAnswer({ text, className = '' }) {
  if (!text) return null;

  const lines = text.split('\n');
  const elements = [];
  let currentList = null; // { type: 'ul' | 'ol', items: [] }

  const flushList = () => {
    if (!currentList) return;
    const ListTag = currentList.type;
    const items = currentList.items;
    const listKey = `list-${elements.length}`;

    elements.push(
      <ListTag key={listKey} className="my-2 space-y-1.5 pl-1">
        {items.map((item, idx) => (
          <li key={idx} className="flex items-start gap-2 text-sm sm:text-base text-slate-700 leading-relaxed">
            {currentList.type === 'ul' ? (
              <span className="mt-2 w-1.5 h-1.5 rounded-full bg-teal-600 shrink-0" aria-hidden="true" />
            ) : (
              <span className="text-xs font-bold text-teal-700 bg-teal-50 border border-teal-200 rounded px-1 shrink-0 mt-0.5">
                {idx + 1}
              </span>
            )}
            <span className="flex-1">{renderInline(item)}</span>
          </li>
        ))}
      </ListTag>
    );
    currentList = null;
  };

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const line = rawLine.trim();

    if (!line) {
      flushList();
      continue;
    }

    // Check for Markdown headings: # Header, ## Header, ### Header
    const hashHeadingMatch = line.match(/^(#{1,4})\s+(.+)$/);
    if (hashHeadingMatch) {
      flushList();
      elements.push(
        <h4 key={`h-${i}`} className="font-bold text-slate-900 text-sm sm:text-base mt-3 mb-1.5 flex items-center gap-1.5 text-teal-900">
          <span className="w-1.5 h-3.5 bg-teal-600 rounded-sm inline-block" />
          {renderInline(hashHeadingMatch[2])}
        </h4>
      );
      continue;
    }

    // Check for bold header lines: **Header:** or **Header**
    const boldHeaderMatch = line.match(/^\*\*([^*]+?)(?::\*\*|\*\*:?)\s*(.*)$/);
    if (boldHeaderMatch) {
      flushList();
      const headerTitle = boldHeaderMatch[1].trim();
      const remainingContent = boldHeaderMatch[2].trim();

      if (!remainingContent) {
        // Standalone section heading
        elements.push(
          <div key={`bh-${i}`} className="font-bold text-slate-900 text-sm sm:text-base mt-3.5 mb-1.5 flex items-center gap-1.5 text-teal-950">
            <span className="w-1 h-3.5 bg-teal-600 rounded-full inline-block" />
            <span>{headerTitle}</span>
          </div>
        );
      } else {
        // Heading with immediate body text: **Summary:** The answer text...
        elements.push(
          <p key={`b-inline-${i}`} className="text-sm sm:text-base text-slate-800 leading-relaxed my-2">
            <strong className="font-bold text-teal-950 mr-1.5">{headerTitle}:</strong>
            <span>{renderInline(remainingContent)}</span>
          </p>
        );
      }
      continue;
    }

    // Check for bullet lists: - item, * item, • item
    const bulletMatch = line.match(/^[-*•]\s+(.+)$/);
    if (bulletMatch) {
      if (!currentList || currentList.type !== 'ul') {
        flushList();
        currentList = { type: 'ul', items: [] };
      }
      currentList.items.push(bulletMatch[1]);
      continue;
    }

    // Check for numbered lists: 1. item, 2. item
    const numberedMatch = line.match(/^(\d+)\.\s+(.+)$/);
    if (numberedMatch) {
      if (!currentList || currentList.type !== 'ol') {
        flushList();
        currentList = { type: 'ol', items: [] };
      }
      currentList.items.push(numberedMatch[2]);
      continue;
    }

    // Regular paragraph line
    flushList();
    elements.push(
      <p key={`p-${i}`} className="text-sm sm:text-base text-slate-800 leading-relaxed my-2">
        {renderInline(line)}
      </p>
    );
  }

  flushList();

  return <div className={`formatted-answer space-y-1 ${className}`}>{elements}</div>;
}
