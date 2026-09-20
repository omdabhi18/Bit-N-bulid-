import React from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function VoiceSpeaker({ text, label = "Listen", className = "" }) {
  const { speak, stopSpeaking, isSpeaking } = useLanguage();

  const handleToggle = (e) => {
    e.stopPropagation();
    if (isSpeaking) {
      stopSpeaking();
    } else {
      speak(text);
    }
  };

  return (
    <button
      onClick={handleToggle}
      title={isSpeaking ? "Stop audio" : "Read aloud (સાંભળો)"}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-all ${
        isSpeaking
          ? 'bg-emerald-600 text-white animate-pulse shadow-sm'
          : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200'
      } ${className}`}
    >
      {isSpeaking ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5 text-emerald-600" />}
      <span>{label}</span>
    </button>
  );
}
