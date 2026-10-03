import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  AlertTriangle,
  CheckCircle2,
  ThumbsUp,
  ThumbsDown,
  BookOpen,
  Globe,
  ShieldAlert,
  ExternalLink,
  Sparkles,
  Info,
  RefreshCw
} from 'lucide-react';

const FALLBACK_LANGUAGES = [
  {
    code: 'en',
    name: 'English',
    native_name: 'English',
    status: 'stable',
    example_questions: [
      'What are the early warning signs of dengue?',
      'How do I prepare ORS solution for diarrhea at home?',
      'What vaccines are given to an infant at birth?',
      'What daily lifestyle habits help manage high blood pressure?'
    ],
    ui_strings: {
      title: 'Multilingual Health FAQ Assistant',
      tagline: 'Reliable, source-grounded health information in Indian local languages',
      placeholder: 'Ask a health question in English...',
      ask_button: 'Ask Question',
      sources_heading: 'Verified Sources & Citations',
      disclaimer_label: 'Medical Disclaimer'
    }
  },
  {
    code: 'hi',
    name: 'Hindi',
    native_name: 'हिन्दी',
    status: 'stable',
    example_questions: [
      'डेंगू बुखार के मुख्य लक्षण क्या हैं और इससे कैसे बचें?',
      'दस्त होने पर ओआरएस (ORS) का घोल कैसे बनाएं?',
      'शिशु के जन्म के समय कौन-से टीके लगाए जाते हैं?',
      'उच्च रक्तचाप (हाई बीपी) को नियंत्रित करने के लिए क्या खाएं?'
    ],
    ui_strings: {
      title: 'बहुभाषी स्वास्थ्य प्रश्नोत्तरी सहायक',
      tagline: 'सत्यापित सार्वजनिक स्वास्थ्य स्रोतों से विश्वसनीय जानकारी',
      placeholder: 'स्वास्थ्य संबंधी प्रश्न पूछें (उदा. डेंगू, ओआरएस, टीकाकरण)...',
      ask_button: 'प्रश्न पूछें',
      sources_heading: 'सत्यापित स्रोत एवं संदर्भ',
      disclaimer_label: 'चिकित्सीय अस्वीकरण'
    }
  },
  {
    code: 'or',
    name: 'Odia',
    native_name: 'ଓଡ଼ିଆ',
    status: 'stable',
    example_questions: [
      'ଡେଙ୍ଗୁ ଜ୍ୱରର ପ୍ରମୁଖ ଲକ୍ଷଣଗୁଡ଼ିକ କ\'ଣ ଏବଂ କିପରି ରକ୍ଷା ପାଇବା?',
      'ତରଳ ଝାଡ଼ା ହେଲେ ଓଆରଏସ୍ (ORS) ଦ୍ରବଣ କିପରି ପ୍ରସ୍ତୁତ କରାଯାଏ?',
      'ନବଜାତ ଶିଶୁକୁ ଜନ୍ମ ସମୟରେ କେଉଁ ଟିକା ଦିଆଯାଏ?',
      'ଉଚ୍ଚ ରକ୍ତଚାପ ନିୟନ୍ତ୍ରଣ କରିବା ପାଇଁ କି ପ୍ରକାର ଖାଦ୍ୟ ଖାଇବା ଉଚିତ?'
    ],
    ui_strings: {
      title: 'ବହୁଭାଷୀ ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନୋତ୍ତର ସହାୟକ',
      tagline: 'ବିଶ୍ୱାସନୀୟ ସରକାରୀ ଓ ସାର୍ବଜନୀନ ସ୍ୱାସ୍ଥ୍ୟ ସୂଚନା',
      placeholder: 'ଓଡ଼ିଆରେ ନିଜର ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ...',
      ask_button: 'ପ୍ରଶ୍ନ ପଠାନ୍ତୁ',
      sources_heading: 'ସତ୍ୟାପିତ ଉତ୍ସ ଏବଂ ପ୍ରମାଣ',
      disclaimer_label: 'ଚିକିତ୍ସା ସମ୍ବନ୍ଧୀୟ ସତର୍କତା'
    }
  }
];

export default function App() {
  const [languages, setLanguages] = useState(FALLBACK_LANGUAGES);
  const [currentLang, setCurrentLang] = useState('en');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [feedbackSent, setFeedbackSent] = useState({});
  const messagesEndRef = useRef(null);

  // Fetch live languages from API
  useEffect(() => {
    fetch('/api/languages')
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && Array.isArray(data) && data.length > 0) {
          setLanguages(data);
        }
      })
      .catch(() => {
        // Fallback to static registry
      });
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const activeLangConfig = languages.find((l) => l.code === currentLang) || languages[0];
  const ui = activeLangConfig.ui_strings || {};

  const handleSend = async (questionText = query) => {
    const textToSend = questionText.trim();
    if (!textToSend || loading) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: textToSend,
      language: currentLang,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: textToSend,
          language: currentLang,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get answer from server');
      }

      const data = await response.json();
      const botMessage = {
        id: data.request_id || Date.now().toString(),
        sender: 'assistant',
        text: data.answer,
        status: data.status,
        citations: data.citations || [],
        disclaimer: data.disclaimer,
        language: data.language,
        is_experimental: data.is_experimental,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          sender: 'assistant',
          text: 'An error occurred while contacting the health assistant service. Please check that the server is running.',
          status: 'error',
          citations: [],
          disclaimer: '',
          language: currentLang,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (requestId, rating) => {
    if (feedbackSent[requestId]) return;
    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          request_id: requestId,
          rating: rating,
        }),
      });
      setFeedbackSent((prev) => ({ ...prev, [requestId]: rating }));
    } catch (err) {
      // Ignore
    }
  };

  const currentFontClass = `lang-${currentLang}`;

  return (
    <div className={`min-h-screen flex flex-col bg-slate-50 text-slate-800 ${currentFontClass}`}>
      {/* Top Navbar */}
      <header className="sticky top-0 z-20 bg-white/90 backdrop-blur-md border-b border-slate-200 px-4 py-3 shadow-sm">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-teal-200 shadow-md">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base sm:text-lg font-bold text-slate-900 leading-tight">
                {ui.title || 'Health FAQ Assistant'}
              </h1>
              <p className="text-xs text-slate-500 hidden sm:block">
                WHO & MoHFW Verified Public Health Guidance
              </p>
            </div>
          </div>

          {/* Language Selector */}
          <div className="flex items-center gap-2">
            <div className="flex items-center bg-slate-100 rounded-lg p-1 border border-slate-200">
              <Globe className="w-4 h-4 text-slate-500 ml-1.5 mr-1" />
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                className="bg-transparent text-xs sm:text-sm font-medium text-slate-700 outline-none pr-2 py-0.5 cursor-pointer"
              >
                {languages.map((l) => (
                  <option key={l.code} value={l.code}>
                    {l.native_name} ({l.name}) {l.status === 'experimental' ? '⚠️' : ''}
                  </option>
                ))}
              </select>
            </div>

            {activeLangConfig.status === 'experimental' && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300 shadow-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5 animate-pulse"></span>
                {ui.status_experimental || 'Experimental'}
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-4 flex flex-col justify-between">
        {/* Experimental Language Notice Banner */}
        {activeLangConfig.status === 'experimental' && (
          <div className="mb-4 p-3 bg-amber-50/90 border border-amber-200 rounded-xl flex items-start gap-2.5 text-xs text-amber-800 shadow-xs">
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold">{activeLangConfig.native_name} ({activeLangConfig.name}) - {ui.status_experimental || 'Experimental Support'}:</span>{' '}
              <span>This language is in active development and experimental benchmark validation. Source coverage and translations may be limited.</span>
            </div>
          </div>
        )}

        {/* Messages Container */}
        <div className="space-y-4 mb-6">
          {messages.length === 0 && (
            <div className="py-8 text-center max-w-lg mx-auto">
              <div className="w-14 h-14 bg-teal-50 border border-teal-200 rounded-2xl flex items-center justify-center mx-auto mb-4 text-teal-600 shadow-sm">
                <Sparkles className="w-7 h-7" />
              </div>
              <h2 className="text-xl font-bold text-slate-900 mb-2">
                {ui.title || 'Multilingual Health FAQ Assistant'}
              </h2>
              <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                {ui.tagline || 'Answers generated strictly from verified WHO and Ministry of Health public documents.'}
              </p>

              {/* Example Question Chips */}
              <div className="text-left">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 block text-center">
                  Recommended Questions / ପରାମର୍ଶିତ ପ୍ରଶ୍ନ / सुझाये गए प्रश्न:
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {(activeLangConfig.example_questions || []).map((ex, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(ex)}
                      className="text-left text-xs sm:text-sm p-3 rounded-xl bg-white border border-slate-200 hover:border-teal-500 hover:bg-teal-50/50 transition-all text-slate-700 shadow-sm flex items-start gap-2"
                    >
                      <span className="text-teal-600 font-bold text-xs mt-0.5">Q:</span>
                      <span>{ex}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Render Chat Messages */}
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              {/* User Bubble */}
              {msg.sender === 'user' && (
                <div className="max-w-[85%] sm:max-w-xl bg-teal-600 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-md text-sm sm:text-base leading-relaxed">
                  {msg.text}
                </div>
              )}

              {/* Assistant Message Card */}
              {msg.sender === 'assistant' && (
                <div className="w-full max-w-2xl">
                  {/* Emergency State */}
                  {msg.status === 'emergency' && (
                    <div className="bg-red-50 border-2 border-red-500 rounded-2xl p-4 sm:p-5 shadow-sm text-red-950">
                      <div className="flex items-center gap-2.5 text-red-700 font-bold text-base mb-2">
                        <ShieldAlert className="w-6 h-6 flex-shrink-0 text-red-600 animate-pulse" />
                        <span>EMERGENCY ALERT / ଆପାତକାଳୀନ ଚେତାବନୀ</span>
                      </div>
                      <p className="text-sm sm:text-base font-semibold text-red-900 mb-4 leading-relaxed">
                        {msg.text}
                      </p>
                      <div className="flex flex-wrap gap-2 pt-2 border-t border-red-200">
                        <a
                          href="tel:112"
                          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white font-bold text-sm shadow-sm transition-colors"
                        >
                          📞 Call 112 (National Emergency)
                        </a>
                        <a
                          href="tel:108"
                          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white font-bold text-sm shadow-sm transition-colors"
                        >
                          🚑 Call 108 (Medical Ambulance)
                        </a>
                      </div>
                    </div>
                  )}

                  {/* Refused State (Dosage / Diagnosis / Out-of-Scope) */}
                  {msg.status === 'refused' && (
                    <div className="bg-amber-50 border border-amber-300 rounded-2xl p-4 sm:p-5 shadow-sm text-amber-950">
                      <div className="flex items-center gap-2 text-amber-800 font-semibold text-sm mb-1.5">
                        <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-600" />
                        <span>Safety Notice / ସତର୍କତା ସୂଚନା</span>
                      </div>
                      <p className="text-sm sm:text-base text-amber-900 leading-relaxed mb-3">
                        {msg.text}
                      </p>
                      <div className="text-xs text-amber-700 bg-amber-100/70 p-2.5 rounded-lg border border-amber-200">
                        ℹ️ This assistant answers general educational health questions only. It does not prescribe medications, calculate dosages, or perform clinical diagnoses.
                      </div>
                    </div>
                  )}

                  {/* Answered State (Grounded Answer + Citations) */}
                  {msg.status === 'answered' && (
                    <div className="bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 shadow-sm">
                      {msg.is_experimental && (
                        <div className="mb-2 inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-amber-100 text-amber-800">
                          ⚠️ Experimental Language Support
                        </div>
                      )}

                      <div className="text-sm sm:text-base text-slate-800 whitespace-pre-wrap leading-relaxed mb-4">
                        {msg.text}
                      </div>

                      {/* Citations List */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="border-t border-slate-100 pt-3 mt-3">
                          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1">
                            <BookOpen className="w-3.5 h-3.5 text-teal-600" />
                            {ui.sources_heading || 'Verified Sources & Citations'}:
                          </span>
                          <div className="flex flex-wrap gap-2">
                            {msg.citations.map((c) => (
                              <a
                                key={c.id}
                                href={c.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-900 border border-teal-200 text-xs font-medium transition-colors shadow-2xs"
                              >
                                <span>[{c.id}] {c.title}</span>
                                <ExternalLink className="w-3 h-3 text-teal-600" />
                              </a>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Medical Disclaimer */}
                      {msg.disclaimer && (
                        <div className="mt-4 pt-3 border-t border-slate-100 flex items-start gap-1.5 text-[11px] text-slate-500 leading-normal">
                          <Info className="w-3.5 h-3.5 text-slate-400 mt-0.5 flex-shrink-0" />
                          <span>{msg.disclaimer}</span>
                        </div>
                      )}

                      {/* Feedback buttons */}
                      <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
                        <span className="text-[11px]">Was this answer helpful?</span>
                        <div className="flex items-center gap-1">
                          <button
                            onClick={() => handleFeedback(msg.id, 'up')}
                            className={`p-1.5 rounded-md hover:bg-slate-100 transition-colors ${
                              feedbackSent[msg.id] === 'up' ? 'text-teal-600 bg-teal-50' : 'text-slate-400'
                            }`}
                            title="Helpful"
                          >
                            <ThumbsUp className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleFeedback(msg.id, 'down')}
                            className={`p-1.5 rounded-md hover:bg-slate-100 transition-colors ${
                              feedbackSent[msg.id] === 'down' ? 'text-rose-600 bg-rose-50' : 'text-slate-400'
                            }`}
                            title="Not helpful"
                          >
                            <ThumbsDown className="w-4 h-4" />
                          </button>
                          {feedbackSent[msg.id] && (
                            <span className="text-[11px] text-teal-600 font-medium ml-1">
                              Thanks for feedback!
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Error State */}
                  {msg.status === 'error' && (
                    <div className="bg-rose-50 border border-rose-200 rounded-2xl p-4 text-rose-800 text-sm">
                      {msg.text}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {loading && (
            <div className="flex items-center gap-2 p-4 bg-white border border-slate-200 rounded-2xl max-w-xs shadow-sm">
              <RefreshCw className="w-4 h-4 text-teal-600 animate-spin" />
              <span className="text-xs text-slate-600 font-medium">
                Searching verified health sources...
              </span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="sticky bottom-2 z-10 pt-2 bg-gradient-to-t from-slate-50 via-slate-50 to-transparent">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="relative bg-white rounded-2xl border border-slate-300 shadow-md focus-within:border-teal-500 focus-within:ring-2 focus-within:ring-teal-200 transition-all p-1.5 flex items-end gap-2"
          >
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={ui.placeholder || 'Ask a health question...'}
              rows={2}
              className="flex-1 resize-none bg-transparent px-3 py-2 text-sm sm:text-base outline-none text-slate-800 placeholder:text-slate-400 min-h-[44px]"
            />
            <button
              type="submit"
              disabled={!query.trim() || loading}
              className="mb-1 p-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 disabled:opacity-40 disabled:hover:bg-teal-600 text-white font-medium shadow-sm transition-colors flex items-center justify-center cursor-pointer"
              title="Send"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          {/* Bottom Persistent Disclaimer */}
          <p className="text-[11px] text-center text-slate-400 mt-2 px-2">
            ⚠️ Informational public health guidance only. Not medical advice. In an emergency, call 112 / 108 immediately.
          </p>
        </div>
      </main>
    </div>
  );
}
