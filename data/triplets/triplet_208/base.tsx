'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
<<<<<<< HEAD
import { ArrowRight, X } from 'lucide-react';;
=======
import { ArrowRight, X, } from 'lucide-react';
>>>>>>> origin/main

export default function CookieConsent() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) {
      setIsVisible(true);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('cookie-consent', 'accepted');
    setIsVisible(false);
  };

  const declineCookies = () => {
    localStorage.setItem('cookie-consent', 'declined');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-900/95 backdrop-blur-sm border-t border-slate-700 p-4 z-50">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex-1 text-center sm:text-left">
          <h3 className="text-lg font-semibold text-white mb-2">
            We use cookies
          </h3>
          <p className="text-gray-300 text-sm">
            We use cookies to enhance your experience and analyze our traffic. 
            <Link href="/privacy" className="text-cyan-400 hover:text-cyan-300 ml-1">
              Learn more
            </Link>
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={declineCookies}
            className="px-4 py-2 text-gray-300 hover:text-white transition-colors"
          >
            Decline
          </button>
          <button
            onClick={acceptCookies}
            className="bg-gradient-to-r from-cyan-500 to-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all duration-300 flex items-center"
          >
            Accept All
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
        <button
          onClick={declineCookies}
          className="absolute top-2 right-2 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}