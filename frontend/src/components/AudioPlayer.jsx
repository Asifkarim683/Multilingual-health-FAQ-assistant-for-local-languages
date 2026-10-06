import React, { useState, useEffect, useRef } from 'react';
import { Volume2, Play, Pause, Square, Loader2 } from 'lucide-react';

const TTS_LABELS = {
  en: { listen: 'Listen', speaking: 'Speaking...', pause: 'Pause', resume: 'Resume', stop: 'Stop' },
  hi: { listen: 'सुनें', speaking: 'बोल रहे हैं...', pause: 'रोकें', resume: 'जारी रखें', stop: 'बंद करें' },
  or: { listen: 'ଶୁଣନ୍ତୁ', speaking: 'ଶୁଣାଉଛି...', pause: 'ଅଟକାନ୍ତୁ', resume: 'ଆଗକୁ ବଢ଼ନ୍ତୁ', stop: 'ବନ୍ଦ କରନ୍ତୁ' },
  bn: { listen: 'শুনুন', speaking: 'শোনাচ্ছে...', pause: 'থামান', resume: 'চালিয়ে যান', stop: 'বন্ধ করুন' },
  te: { listen: 'వినండి', speaking: 'వినిపిస్తోంది...', pause: 'ఆపండి', resume: 'కొనసాగించండి', stop: 'ముగించండి' },
  ta: { listen: 'கேளுங்கள்', speaking: 'பேசுகிறது...', pause: 'நிறுத்துங்கள்', resume: 'தொடருங்கள்', stop: 'முடி' },
};

export default function AudioPlayer({ text, language = 'en', className = '' }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [rate, setRate] = useState(1.0);
  const audioRef = useRef(null);

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

  // Stop any playing audio on unmount or when text / language changes
  useEffect(() => {
    return () => {
      stopAudio();
    };
  }, [text, language]);

  const stopAudio = () => {
    if (audioRef.current) {
      try {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      } catch (e) {
        // Ignore aborts
      }
    }
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoading(false);
  };

  const handlePlay = () => {
    const cleanText = getCleanText(text);
    if (!cleanText) return;

    if (!audioRef.current) return;

    // If currently paused, resume playback directly
    if (isPaused && audioRef.current.src) {
      audioRef.current.playbackRate = rate;
      audioRef.current
        .play()
        .then(() => {
          setIsPlaying(true);
          setIsPaused(false);
        })
        .catch((err) => {
          console.warn('Resume failed, restarting audio:', err);
          startNewAudio(cleanText);
        });
      return;
    }

    startNewAudio(cleanText);
  };

  const startNewAudio = (cleanText) => {
    const audioUrl = `/api/tts?text=${encodeURIComponent(cleanText)}&language=${language}`;
    const audio = audioRef.current;
    if (!audio) return;

    setIsLoading(true);
    setIsPaused(false);

    if (audio.src !== window.location.origin + audioUrl && audio.src !== audioUrl) {
      audio.src = audioUrl;
    }
    audio.playbackRate = rate;

    audio
      .play()
      .then(() => {
        setIsLoading(false);
        setIsPlaying(true);
      })
      .catch((err) => {
        console.warn('Server TTS playback error:', err);
        // Fallback to browser Web Speech API for English / Hindi if available
        if (typeof window !== 'undefined' && 'speechSynthesis' in window && (language === 'en' || language === 'hi')) {
          speakWithWebSpeechFallback(cleanText);
        } else {
          setIsLoading(false);
          setIsPlaying(false);
        }
      });
  };

  const speakWithWebSpeechFallback = (cleanText) => {
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = language === 'hi' ? 'hi-IN' : 'en-IN';
      utterance.rate = rate;
      utterance.onstart = () => {
        setIsLoading(false);
        setIsPlaying(true);
        setIsPaused(false);
      };
      utterance.onend = () => {
        setIsPlaying(false);
        setIsPaused(false);
      };
      utterance.onerror = () => {
        setIsPlaying(false);
        setIsLoading(false);
      };
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      setIsLoading(false);
      setIsPlaying(false);
    }
  };

  const handlePause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPaused(true);
      setIsPlaying(false);
    }
  };

  const toggleSpeed = () => {
    const speeds = [0.85, 1.0, 1.25];
    const currentIdx = speeds.indexOf(rate);
    const nextRate = speeds[(currentIdx + 1) % speeds.length];
    setRate(nextRate);
    if (audioRef.current) {
      audioRef.current.playbackRate = nextRate;
    }
  };

  return (
    <div className={`inline-flex items-center gap-1.5 p-1 rounded-xl bg-slate-50 border border-slate-200/80 shadow-2xs ${className}`}>
      {/* Hidden HTML5 Native Audio Element */}
      <audio
        ref={audioRef}
        preload="none"
        onPlaying={() => {
          setIsLoading(false);
          setIsPlaying(true);
          setIsPaused(false);
        }}
        onWaiting={() => setIsLoading(true)}
        onPause={() => {
          if (!audioRef.current?.ended) {
            setIsPaused(true);
          }
        }}
        onEnded={() => {
          setIsPlaying(false);
          setIsPaused(false);
          setIsLoading(false);
        }}
        onError={(e) => {
          console.warn('Audio tag error:', e);
          setIsLoading(false);
          setIsPlaying(false);
        }}
      />

      {/* Play / Listen Button */}
      {!isPlaying && !isPaused && !isLoading && (
        <button
          type="button"
          onClick={handlePlay}
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 text-xs font-semibold transition-all border border-teal-200/70 cursor-pointer hover:shadow-2xs active:scale-95"
          title={`${labels.listen} (${language.toUpperCase()})`}
        >
          <Volume2 className="w-3.5 h-3.5 text-teal-600" />
          <span>{labels.listen}</span>
        </button>
      )}

      {/* Loading State Spinner */}
      {isLoading && (
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 text-xs font-medium">
          <Loader2 className="w-3.5 h-3.5 text-teal-600 animate-spin" />
          <span>{language === 'or' ? 'ଶୁଣାଯାଉଛି...' : 'Loading audio...'}</span>
        </div>
      )}

      {/* Active Playing / Paused State Controls */}
      {(isPlaying || isPaused) && !isLoading && (
        <div className="flex items-center gap-1.5">
          {/* Animated Equalizer Sound Bars */}
          <div className="flex items-center gap-0.5 px-2 py-1 bg-teal-100/70 rounded-md">
            <span className={`w-1 h-3 bg-teal-600 rounded-full ${isPlaying ? 'animate-pulse' : 'h-1.5'}`}></span>
            <span className={`w-1 h-4 bg-teal-500 rounded-full ${isPlaying ? 'animate-bounce' : 'h-2'}`}></span>
            <span className={`w-1 h-2 bg-teal-600 rounded-full ${isPlaying ? 'animate-pulse' : 'h-1.5'}`}></span>
          </div>

          <span className="text-xs font-semibold text-teal-900 hidden sm:inline">
            {isPaused ? labels.pause : labels.speaking}
          </span>

          {/* Pause / Resume Button */}
          {isPaused ? (
            <button
              type="button"
              onClick={handlePlay}
              className="p-1 rounded-md bg-white hover:bg-teal-50 text-teal-700 border border-slate-200 cursor-pointer shadow-2xs"
              title={labels.resume}
            >
              <Play className="w-3.5 h-3.5 fill-current" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handlePause}
              className="p-1 rounded-md bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 cursor-pointer shadow-2xs"
              title={labels.pause}
            >
              <Pause className="w-3.5 h-3.5 fill-current" />
            </button>
          )}

          {/* Stop Button */}
          <button
            type="button"
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
        type="button"
        onClick={toggleSpeed}
        className="px-1.5 py-0.5 rounded text-[10px] font-bold text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 transition-colors cursor-pointer"
        title="Change Speech Speed"
      >
        {rate}x
      </button>
    </div>
  );
}
