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
  RefreshCw,
  Volume2,
  Mic,
  MicOff
} from 'lucide-react';
import AudioPlayer from './components/AudioPlayer';

const STT_LANG_MAP = {
  en: 'en-IN',
  hi: 'hi-IN',
  bn: 'bn-IN',
  te: 'te-IN',
  ta: 'ta-IN',
  or: 'or-IN',
};

const STT_PROMPTS = {
  en: { listening: 'Listening in English... Speak your question', button: 'Speak Question (Mic)', stop: 'Stop' },
  hi: { listening: 'हिन्दी में सुन रहे हैं... अपना प्रश्न बोलें', button: 'बोलकर पूछें', stop: 'रोकें' },
  or: { listening: 'ଓଡ଼ିଆରେ ଶୁଣୁଛି... ଆପଣଙ୍କ ପ୍ରଶ୍ନ କୁହନ୍ତୁ', button: 'କୁହନ୍ତୁ (ମାଇକ୍)', stop: 'ବନ୍ଦ କରନ୍ତୁ' },
  bn: { listening: 'বাংলায় শুনছি... আপনার প্রশ্ন বলুন', button: 'কথা বলুন (মাইক)', stop: 'থামান' },
  te: { listening: 'తెలుగులో వింటున్నాను... మీ ప్రశ్న మాట్లాడండి', button: 'మాట్లాడండి', stop: 'ఆపండి' },
  ta: { listening: 'தமிழில் கேட்கிறது... உங்கள் கேள்வியைக் கூறுங்கள்', button: 'பேசுங்கள்', stop: 'நிறுத்து' },
};

const FALLBACK_LANGUAGES = [
  {
    code: 'en',
    name: 'English',
    native_name: 'English',
    status: 'stable',
    example_questions: [
      'What are the early warning signs and symptoms of dengue?',
      'How should Oral Rehydration Solution (ORS) be prepared for diarrhea?',
      'What is the recommended immunization schedule for an infant\'s first 6 months?',
      'What dietary and lifestyle habits help control high blood pressure?'
    ],
    ui_strings: {
      title: 'Multilingual Health FAQ Assistant',
      tagline: 'Reliable, source-grounded health information in Indian local languages',
      placeholder: 'Ask a health question (e.g. dengue symptoms, fever, ORS, vaccines)...',
      ask_button: 'Ask Question',
      sources_heading: 'Verified Sources & Citations',
      disclaimer_label: 'Medical Disclaimer',
      status_stable: 'Verified',
      status_experimental: 'Experimental'
    }
  },
  {
    code: 'hi',
    name: 'Hindi',
    native_name: 'हिन्दी',
    status: 'stable',
    example_questions: [
      'डेंगू बुखार के मुख्य लक्षण क्या हैं और इससे कैसे बचें?',
      'दस्त और उल्टी होने पर ओआरएस (ORS) का घोल कैसे बनाएं?',
      'शिशु के जन्म के पहले 6 महीनों में कौन-से टीके लगवाने चाहिए?',
      'उच्च रक्तचाप (हाई बीपी) को नियंत्रित करने के लिए क्या खाना चाहिए?'
    ],
    ui_strings: {
      title: 'बहुभाषी स्वास्थ्य प्रश्नोत्तरी सहायक',
      tagline: 'सत्यापित सार्वजनिक स्वास्थ्य स्रोतों से विश्वसनीय जानकारी',
      placeholder: 'स्वास्थ्य संबंधी प्रश्न पूछें (उदा. डेंगू, ओआरएस, टीकाकरण)...',
      ask_button: 'प्रश्न पूछें',
      sources_heading: 'सत्यापित स्रोत एवं संदर्भ',
      disclaimer_label: 'चिकित्सीय अस्वीकरण',
      status_stable: 'सत्यापित',
      status_experimental: 'प्रायोगिक'
    }
  },
  {
    code: 'or',
    name: 'Odia',
    native_name: 'ଓଡ଼ିଆ',
    status: 'stable',
    example_questions: [
      'ଡେଙ୍ଗୁ ଜ୍ୱରର ପ୍ରମୁଖ ଲକ୍ଷଣଗୁଡ଼ିକ କ\'ଣ ଏବଂ ଏଥିରୁ କିପରି ରକ୍ଷା ପାଇବା?',
      'ତରଳ ଝାଡ଼ା ହେଲେ ଓଆରଏସ୍ (ORS) ଦ୍ରବଣ କିପରି ପ୍ରସ୍ତୁତ କରାଯାଏ?',
      'ନବଜାତ ଶିଶୁ ପାଇଁ ପ୍ରଥମ ୬ ମାସ ମଧ୍ୟରେ କେଉଁ ଟିକା ଦିଆଯାଏ?',
      'ଉଚ୍ଚ ରକ୍ତଚାପ ନିୟନ୍ତ୍ରଣ କରିବା ପାଇଁ କି ପ୍ରକାର ଖାଦ୍ୟ ଖାଇବା ଉଚିତ?'
    ],
    ui_strings: {
      title: 'ବହୁଭାଷୀ ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନୋତ୍ତର ସହାୟକ',
      tagline: 'ବିଶ୍ୱାସନୀୟ ସରକାରୀ ଓ ସାର୍ବଜନୀନ ସ୍ୱାସ୍ଥ୍ୟ ସୂଚନା',
      placeholder: 'ଓଡ଼ିଆରେ ନିଜର ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ...',
      ask_button: 'ପ୍ରଶ୍ନ ପଠାନ୍ତୁ',
      sources_heading: 'ସତ୍ୟାପିତ ଉତ୍ସ ଏବଂ ପ୍ରମାଣ',
      disclaimer_label: 'ଚିକିତ୍ସା ସମ୍ବନ୍ଧୀୟ ସତର୍କତା',
      status_stable: 'ପରୀକ୍ଷିତ (Verified)',
      status_experimental: 'ପରୀକ୍ଷାମୂଳକ (Experimental)'
    }
  },
  {
    code: 'bn',
    name: 'Bengali',
    native_name: 'বাংলা',
    status: 'experimental',
    example_questions: [
      'ডেঙ্গু জ্বরের প্রধান লক্ষণগুলি কি কি এবং কীভাবে প্রতিরোধ করবেন?',
      'ডায়রিয়া হলে ওআরএস (ORS) কীভাবে তৈরি করবেন?',
      'শিশুর জন্মের সময় এবং প্রথম ৬ মাসে কোন টিকা দেওয়া হয়?',
      'উচ্চ রক্তচাপ বা ডায়াবেটিস নিয়ন্ত্রণে কী ধরনের খাবার খাওয়া উচিত?'
    ],
    ui_strings: {
      title: 'বহুভাষিক স্বাস্থ্য FAQ সহকারী',
      tagline: 'যাচাইকৃত জনস্বাস্থ্য উৎস থেকে নির্ভরযোগ্য তথ্য',
      placeholder: 'স্বাস্থ্য সম্পর্কিত প্রশ্ন জিজ্ঞাসা করুন...',
      ask_button: 'প্রশ্ন পাঠান',
      sources_heading: 'যাচাইকৃত উৎস',
      disclaimer_label: 'চিকিৎসা সংক্রান্ত দাবিত্যাগ',
      status_stable: 'যাচাইকৃত',
      status_experimental: 'পরীক্ষামূলক (Experimental)'
    }
  },
  {
    code: 'te',
    name: 'Telugu',
    native_name: 'తెలుగు',
    status: 'experimental',
    example_questions: [
      'డెంగ్యూ జ్వరం ముఖ్య లక్షణాలు ఏమిటి మరియు నివారణ చర్యలు?',
      'అతిసార సమయంలో ఇంట్లోనే ORS ద్రావణం ఎలా తయారు చేయాలి?',
      'నవజాత శిశువుకు పుట్టినప్పుడు మరియు మొదటి 6 నెలల్లో ఏ టీకాలు వేయాలి?',
      'అధిక రక్తపోటు మరియు మధుమేహం నియంత్రణకు ఎటువంటి ఆహారం తీసుకోవాలి?'
    ],
    ui_strings: {
      title: 'బహుభాషా ఆరోగ్య FAQ సహాయకుడు',
      tagline: 'ధృవీకరించబడిన ప్రజారోగ్య వనరుల నుండి సమాచారం',
      placeholder: 'మీ ఆరోగ్య ప్రశ్నను అడగండి...',
      ask_button: 'ప్రశ్న పంపండి',
      sources_heading: 'ధృవీకరించబడిన వనరులు',
      disclaimer_label: 'వైద్య నిరాకరణ',
      status_stable: 'ధృవీకరించబడింది',
      status_experimental: 'ప్రయోగాత్మక (Experimental)'
    }
  },
  {
    code: 'ta',
    name: 'Tamil',
    native_name: 'தமிழ்',
    status: 'experimental',
    example_questions: [
      'டெங்கு காய்ச்சலின் முக்கிய அறிகுறிகள் என்ன மற்றும் தடுப்பு முறைகள்?',
      'வயிற்றுப்போக்கின் போது வீட்டிலேயே ORS கரைசலை எவ்வாறு தயாரிப்பது?',
      'குழந்தை பிறந்தவுடன் மற்றும் முதல் 6 மாதங்களில் போட வேண்டிய தடுப்பூசிகள் எவை?',
      'உயர் இரத்த அழுத்தம் மற்றும் சர்க்கரை நோயைக் கட்டுப்படுத்த என்ன சாப்பிட வேண்டும்?'
    ],
    ui_strings: {
      title: 'பன்மொழி சுகாதார FAQ உதவியாளர்',
      tagline: 'நம்பகமான பொது சுகாதார ஆதாரங்கள்',
      placeholder: 'சுகாதாரம் தொடர்பான கேள்விகளைக் கேளுங்கள்...',
      ask_button: 'கேள்வி கேட்க',
      sources_heading: 'சரிபார்க்கப்பட்ட ஆதாரங்கள்',
      disclaimer_label: 'மருத்துவ மறுப்பு',
      status_stable: 'சரிபார்க்கப்பட்டது',
      status_experimental: 'பரிசோதனை (Experimental)'
    }
  }
];

export default function App() {
  const [languages, setLanguages] = useState(FALLBACK_LANGUAGES);
  const [currentLang, setCurrentLang] = useState('en');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [switchingLang, setSwitchingLang] = useState(false);
  const [messages, setMessages] = useState([]);
  const [feedbackSent, setFeedbackSent] = useState({});
  const [isListening, setIsListening] = useState(false);
  const [sttSupported, setSttSupported] = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const qaCacheRef = useRef(new Map());

  // Helper: map a question to a language-agnostic canonical key for instant caching
  const getCanonicalKey = (text) => {
    const trimmed = (text || '').trim().toLowerCase();
    for (const langObj of languages) {
      const idx = (langObj.example_questions || []).findIndex(
        (eq) => eq.trim().toLowerCase() === trimmed
      );
      if (idx !== -1) {
        return `ex_${idx}`;
      }
    }
    return `custom_${trimmed}`;
  };

  // Check Web Speech Recognition support on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        setSttSupported(true);
      }
    }
  }, []);

  const handleToggleVoiceInput = () => {
    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech-to-Text is supported in Google Chrome, Microsoft Edge, Safari, and Android browsers.');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      recognition.lang = STT_LANG_MAP[currentLang] || 'en-IN';
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((result) => result[0].transcript)
          .join('');
        setQuery(transcript);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (err) {
      console.error('Failed to start speech recognition:', err);
      setIsListening(false);
    }
  };

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

  // Handle seamless language switching with automatic re-translation/re-generation
  const handleLanguageChange = async (newLang) => {
    if (newLang === currentLang && messages.length > 0) return;
    setCurrentLang(newLang);

    const targetLangConfig = languages.find((l) => l.code === newLang) || languages[0];

    // If query input contains an example question, translate the input box too
    if (query.trim()) {
      for (const langObj of languages) {
        const idx = (langObj.example_questions || []).findIndex(
          (eq) => eq.trim().toLowerCase() === query.trim().toLowerCase()
        );
        if (idx !== -1 && targetLangConfig.example_questions && targetLangConfig.example_questions[idx]) {
          setQuery(targetLangConfig.example_questions[idx]);
          break;
        }
      }
    }

    // If no conversation messages yet, just update the language state
    if (messages.length === 0) return;

    // Find the latest user question in chat history
    const userMessages = messages.filter((m) => m.sender === 'user');
    if (userMessages.length === 0) return;

    const lastUserMsg = userMessages[userMessages.length - 1];
    const canonicalKey = getCanonicalKey(lastUserMsg.text);

    let questionToSend = lastUserMsg.text;
    if (canonicalKey.startsWith('ex_')) {
      const idx = parseInt(canonicalKey.replace('ex_', ''), 10);
      if (targetLangConfig.example_questions && targetLangConfig.example_questions[idx]) {
        questionToSend = targetLangConfig.example_questions[idx];
      }
    }

    // Check if response is already cached for this target language (instant switch 0ms)
    const cacheKey = `${canonicalKey}_${newLang}`;
    if (qaCacheRef.current.has(cacheKey)) {
      const cachedBotMsg = qaCacheRef.current.get(cacheKey);
      setMessages((prev) => {
        const next = [...prev];
        for (let i = next.length - 1; i >= 0; i--) {
          if (next[i].sender === 'user') {
            next[i] = { ...next[i], text: questionToSend, language: newLang };
            break;
          }
        }
        for (let i = next.length - 1; i >= 0; i--) {
          if (next[i].sender === 'assistant') {
            next[i] = { ...cachedBotMsg, id: Date.now().toString() };
            break;
          }
        }
        return next;
      });
      return;
    }

    // Update the user question bubble in chat to the target language
    setMessages((prev) => {
      const next = [...prev];
      for (let i = next.length - 1; i >= 0; i--) {
        if (next[i].sender === 'user') {
          next[i] = {
            ...next[i],
            text: questionToSend,
            language: newLang,
          };
          break;
        }
      }
      return next;
    });

    setSwitchingLang(true);

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: questionToSend,
          language: newLang,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to retrieve answer in desired language');
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

      qaCacheRef.current.set(cacheKey, botMessage);

      setMessages((prev) => {
        const next = [...prev];
        for (let i = next.length - 1; i >= 0; i--) {
          if (next[i].sender === 'assistant') {
            next[i] = botMessage;
            break;
          }
        }
        return next;
      });
    } catch (err) {
      console.error('Error switching language:', err);
    } finally {
      setSwitchingLang(false);
    }
  };

  const handleSend = async (questionText = query) => {
    const textToSend = questionText.trim();
    if (!textToSend || loading || switchingLang) return;

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

      const canonicalKey = getCanonicalKey(textToSend);
      qaCacheRef.current.set(`${canonicalKey}_${currentLang}`, botMessage);

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
                disabled={loading || switchingLang}
                onChange={(e) => handleLanguageChange(e.target.value)}
                className="bg-transparent text-xs sm:text-sm font-medium text-slate-700 outline-none pr-2 py-0.5 cursor-pointer disabled:opacity-50"
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
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <div className="flex items-center gap-2.5 text-red-700 font-bold text-base">
                          <ShieldAlert className="w-6 h-6 flex-shrink-0 text-red-600 animate-pulse" />
                          <span>EMERGENCY ALERT / ଆପାତକାଳୀନ ଚେତାବନୀ</span>
                        </div>
                        <AudioPlayer text={msg.text} language={msg.language || currentLang} className="bg-red-100/70 border-red-200" />
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
                      <div className="flex items-center justify-between gap-2 mb-1.5">
                        <div className="flex items-center gap-2 text-amber-800 font-semibold text-sm">
                          <AlertTriangle className="w-5 h-5 flex-shrink-0 text-amber-600" />
                          <span>Safety Notice / ସତର୍କତା ସୂଚନା</span>
                        </div>
                        <AudioPlayer text={msg.text} language={msg.language || currentLang} className="bg-amber-100/70 border-amber-200" />
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
                      {switchingLang ? (
                        <div className="py-7 px-4 flex flex-col items-center justify-center text-center gap-2.5">
                          <div className="w-9 h-9 rounded-full bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600">
                            <RefreshCw className="w-5 h-5 animate-spin" />
                          </div>
                          <div>
                            <p className="text-sm font-semibold text-slate-800">
                              {activeLangConfig.native_name} ({activeLangConfig.name}) - Generating guidance...
                            </p>
                            <p className="text-xs text-slate-500 mt-0.5">
                              Translating answer and retrieving verified health sources
                            </p>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="flex items-center justify-between gap-2 mb-3 pb-2 border-b border-slate-100">
                            <AudioPlayer text={msg.text} language={msg.language || currentLang} />
                            {msg.is_experimental && (
                              <div className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold bg-amber-100 text-amber-800 shrink-0">
                                ⚠️ Experimental
                              </div>
                            )}
                          </div>

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

                          {/* Quick Language Switcher Bar on Answer */}
                          <div className="mt-3.5 pt-2.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2">
                            <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-500">
                              <Globe className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                              <span className="text-[11px] font-medium text-slate-500">Read in:</span>
                              <div className="flex flex-wrap gap-1">
                                {languages.map((l) => (
                                  <button
                                    key={l.code}
                                    type="button"
                                    disabled={switchingLang || loading}
                                    onClick={() => handleLanguageChange(l.code)}
                                    className={`px-2 py-0.5 rounded-md text-xs transition-all cursor-pointer ${
                                      currentLang === l.code
                                        ? 'bg-teal-600 text-white font-semibold shadow-xs'
                                        : 'bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium'
                                    }`}
                                  >
                                    {l.native_name}
                                  </button>
                                ))}
                              </div>
                            </div>
                          </div>

                          {/* Medical Disclaimer */}
                          {msg.disclaimer && (
                            <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-start gap-1.5 text-[11px] text-slate-500 leading-normal">
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
                        </>
                      )}
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

          {/* Loading indicator for new question submission */}
          {loading && !switchingLang && (
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
          {/* Active Voice Input Pill Indicator */}
          {isListening && (
            <div className="mb-2 px-3.5 py-2 rounded-xl bg-red-50 border border-red-300 text-red-900 text-xs font-semibold flex items-center justify-between shadow-sm animate-pulse">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-red-600 animate-ping"></span>
                <span>{(STT_PROMPTS[currentLang] || STT_PROMPTS.en).listening}</span>
              </div>
              <button
                type="button"
                onClick={handleToggleVoiceInput}
                className="text-[11px] underline font-bold text-red-700 hover:text-red-900 cursor-pointer ml-2"
              >
                {(STT_PROMPTS[currentLang] || STT_PROMPTS.en).stop}
              </button>
            </div>
          )}

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="relative bg-white rounded-2xl border border-slate-300 shadow-md focus-within:border-teal-500 focus-within:ring-2 focus-within:ring-teal-200 transition-all p-1.5 flex items-end gap-1.5"
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

            {/* Voice Input (Microphone) Button */}
            <button
              type="button"
              onClick={handleToggleVoiceInput}
              className={`mb-1 p-2.5 rounded-xl border transition-all flex items-center justify-center cursor-pointer ${
                isListening
                  ? 'bg-red-600 text-white border-red-600 ring-4 ring-red-200 animate-pulse'
                  : 'bg-slate-100 hover:bg-teal-50 text-slate-600 hover:text-teal-700 border-slate-200 hover:border-teal-300 shadow-2xs'
              }`}
              title={(STT_PROMPTS[currentLang] || STT_PROMPTS.en).button}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>

            {/* Send Button */}
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
