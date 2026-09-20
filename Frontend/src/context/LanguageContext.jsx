import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from '../data/translations';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('krishi_lang') || 'en';
  });
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    localStorage.setItem('krishi_lang', language);
  }, [language]);

  const t = (keyPath, fallback = "") => {
    const keys = keyPath.split('.');
    let current = translations[language] || translations['en'];
    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // fallback to English
        let enFallback = translations['en'];
        for (const k of keys) {
          if (enFallback && enFallback[k] !== undefined) {
            enFallback = enFallback[k];
          } else {
            return fallback || keyPath;
          }
        }
        return enFallback;
      }
    }
    return current;
  };

  const speak = (text) => {
    if (!('speechSynthesis' in window)) {
      alert("Text-to-speech not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    if (!text) return;

    const utterance = new SpeechSynthesisUtterance(text);
    if (language === 'gu') {
      utterance.lang = 'gu-IN';
    } else if (language === 'hi') {
      utterance.lang = 'hi-IN';
    } else {
      utterance.lang = 'en-IN';
    }
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, speak, stopSpeaking, isSpeaking }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
