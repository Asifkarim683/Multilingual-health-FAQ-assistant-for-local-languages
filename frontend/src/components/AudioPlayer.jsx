import React, { useState, useEffect, useRef } from 'react';
import { Volume2, VolumeX, Play, Pause, Square, Loader2 } from 'lucide-react';

const TTS_LABELS = {
  en: { listen: 'Listen', speaking: 'Speaking...', pause: 'Pause', resume: 'Resume', stop: 'Stop' },
  hi: { listen: 'सुनें', speaking: 'बोल रहे हैं...', pause: 'रोकें', resume: 'जारी रखें', stop: 'बंद करें' },
  or: { listen: 'ଶୁଣନ୍ତୁ', speaking: 'ଶୁଣାଉଛି...', pause: 'ଅଟକାନ୍ତୁ', resume: 'ଆଗକୁ ବଢ଼ନ୍ତୁ', stop: 'ବନ୍ଦ କରନ୍ତୁ' },
  bn: { listen: 'শুনুন', speaking: 'শোনাচ্ছে...', pause: 'থামান', resume: 'চালিয়ে যান', stop: 'বন্ধ করুন' },
  te: { listen: 'వినండి', speaking: 'వినిపిస్తోంది...', pause: 'ఆపండి', resume: 'కొనసాగించండి', stop: 'ముగించండి' },
  ta: { listen: 'கேளுங்கள்', speaking: 'பேசுகிறது...', pause: 'நிறுத்துங்கள்', resume: 'தொடருங்கள்', stop: 'முடி' },
};

const BCP47_LANG_MAP = {
  en: ['en-IN', 'en-US', 'en-GB', 'en'],
  hi: ['hi-IN', 'hi'],
  bn: ['bn-IN', 'bn-BD', 'bn'],
  te: ['te-IN', 'te'],
  ta: ['ta-IN', 'ta-LK', 'ta'],
  or: ['or-IN', 'or', 'hi-IN'], // Odia fallback to Indic phonetics if voice missing
};

export default function AudioPlayer({ text, language = 'en', className = '' }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [rate, setRate] = useState(0.9); // 0.9x is optimal for medical clarity
  const audioRef = useRef(null);
  const isSpeechSynthesisSupported = typeof window !== 'undefined' && 'speechSynthesis' in window;

  const labels = TTS_LABELS[language] || TTS_LABELS.en;

  // Clean text of markdown, citations [1], URLs, and formatting
  const getCleanText = (raw) => {
    if (!raw) return '';
    return raw
      .replace(/\[\d+\]/g, '') // remove citation numbers [1]
      .replace(/\[.*?\]\(.*?\)/g, '') // remove markdown links
      .replace(/[*#_`>]/g, '') // remove markdown symbols
      .replace(/\s+/g, ' ')
      .trim();
  };

  // Stop any playing audio on unmount or text change
  useEffect(() => {
    return () => {
      stopAudio();
    };
  }, [text, language]);

  const stopAudio = () => {
    if (isSpeechSynthesisSupported) {
      window.speechSynthesis.cancel();
    }
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoading(false);
  };

  // Play using Web Speech API (Client-side)
  const speakWithWebSpeech = (cleanText) => {
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    const targetTags = BCP47_LANG_MAP[language] || ['en-IN', 'en-US'];

    // Find best voice
    const voices = window.speechSynthesis.getVoices();
    let selectedVoice = null;
    for (const tag of targetTags) {
      selectedVoice = voices.find(
        (v) => v.lang.toLowerCase().replace('_', '-') === tag.toLowerCase()
      );
      if (selectedVoice) break;
    }

    if (selectedVoice) {
      utterance.voice = selectedVoice;
      utterance.lang = selectedVoice.lang;
    } else {
      utterance.lang = targetTags[0];
    }

    utterance.rate = rate;
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      setIsPlaying(true);
      setIsPaused(false);
      setIsLoading(false);
    };

    utterance.onpause = () => {
      setIsPaused(true);
    };

    utterance.onresume = () => {
      setIsPaused(false);
    };

    utterance.onend = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    utterance.onerror = (e) => {
      console.warn('SpeechSynthesis error, falling back to server TTS:', e);
      speakWithServerTTS(cleanText);
    };

    window.speechSynthesis.speak(utterance);
  };

  // Fallback: Play using Backend Server MP3 Streaming (/api/tts)
  const speakWithServerTTS = (cleanText) => {
    setIsLoading(true);
    if (!audioRef.current) {
      audioRef.current = new Audio();
    }

    const audioUrl = `/api/tts?text=${encodeURIComponent(cleanText)}&language=${language}`;
    audioRef.current.src = audioUrl;
    audioRef.current.playbackRate = rate;

    audioRef.current.oncanplay = () => {
      setIsLoading(false);
      setIsPlaying(true);
      audioRef.current.play().catch(() => {
        setIsPlaying(false);
        setIsLoading(false);
      });
    };

    audioRef.current.onended = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };

    audioRef.current.onerror = () => {
      setIsPlaying(false);
      setIsPaused(false);
      setIsLoading(false);
    };

    audioRef.current.load();
  };

  const handlePlay = () => {
    const cleanText = getCleanText(text);
    if (!cleanText) return;

    if (isPaused) {
      if (isSpeechSynthesisSupported && window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
        setIsPaused(false);
        return;
      }
      if (audioRef.current && audioRef.current.paused) {
        audioRef.current.play();
        setIsPaused(false);
        return;
      }
    }

    if (isSpeechSynthesisSupported) {
      speakWithWebSpeech(cleanText);
    } else {
      speakWithServerTTS(cleanText);
    }
  };

  const handlePause = () => {
    if (isSpeechSynthesisSupported && window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    } else if (audioRef.current && !audioRef.current.paused) {
      audioRef.current.pause();
      setIsPaused(true);
    }
  };

  const toggleSpeed = () => {
    const speeds = [0.85, 1.0, 1.15];
    const currentIdx = speeds.indexOf(rate);
    const nextRate = speeds[(currentIdx + 1) % speeds.length];
    setRate(nextRate);
    if (audioRef.current) {
      audioRef.current.playbackRate = nextRate;
    }
  };

  return (
    <div className={`inline-flex items-center gap-1.5 p-1 rounded-xl bg-slate-50 border border-slate-200/80 shadow-2xs ${className}`}>
      {/* Play / Listen Button */}
      {!isPlaying && !isLoading && (
        <button
          onClick={handlePlay}
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 text-xs font-semibold transition-all border border-teal-200/70 cursor-pointer hover:shadow-2xs active:scale-95"
          title={`${labels.listen} (${language.toUpperCase()})`}
        >
          <Volume2 className="w-3.5 h-3.5 text-teal-600" />
          <span>{labels.listen}</span>
        </button>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 text-xs font-medium">
          <Loader2 className="w-3.5 h-3.5 text-teal-600 animate-spin" />
          <span>Loading...</span>
        </div>
      )}

      {/* Active Playing State Controls */}
      {isPlaying && (
        <div className="flex items-center gap-1.5">
          {/* Animated Equalizer Sound Bars */}
          <div className="flex items-center gap-0.5 px-2 py-1 bg-teal-100/70 rounded-md">
            <span className="w-1 h-3 bg-teal-600 rounded-full animate-pulse"></span>
            <span className="w-1 h-4 bg-teal-500 rounded-full animate-bounce"></span>
            <span className="w-1 h-2 bg-teal-600 rounded-full animate-pulse"></span>
          </div>

          <span className="text-xs font-semibold text-teal-900 hidden sm:inline">
            {labels.speaking}
          </span>

          {/* Pause / Resume Button */}
          {isPaused ? (
            <button
              onClick={handlePlay}
              className="p-1 rounded-md bg-white hover:bg-teal-50 text-teal-700 border border-slate-200 cursor-pointer shadow-2xs"
              title={labels.resume}
            >
              <Play className="w-3.5 h-3.5 fill-current" />
            </button>
          ) : (
            <button
              onClick={handlePause}
              className="p-1 rounded-md bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 cursor-pointer shadow-2xs"
              title={labels.pause}
            >
              <Pause className="w-3.5 h-3.5 fill-current" />
            </button>
          )}

          {/* Stop Button */}
          <button
            onClick={stopAudio}
            className="p-1 rounded-md bg-white hover:bg-red-50 text-red-600 border border-slate-200 cursor-pointer shadow-2xs"
            title={labels.stop}
          >
            <Square className="w-3.5 h-3.5 fill-current" />
          </button>
        </div>
      )}

      {/* Speech Speed Adjustment Chip */}
      <button
        onClick={toggleSpeed}
        className="px-1.5 py-0.5 rounded text-[10px] font-bold text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 transition-colors cursor-pointer"
        title="Change Speech Speed"
      >
        {rate}x
      </button>
    </div>
  );
}
