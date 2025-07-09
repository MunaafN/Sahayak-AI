// Essential Indian Languages Configuration
// This file contains the core languages supported by the application

export const languages = [
  // Core supported languages
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' },
  { code: 'ur', name: 'Urdu', nativeName: 'اردو' }
];

// Get languages formatted for select options
export const getLanguageOptions = () => {
  return languages.map(lang => ({
    value: lang.code,
    label: `${lang.name} / ${lang.nativeName}`
  }));
};

// Get language name by code
export const getLanguageName = (code) => {
  const lang = languages.find(l => l.code === code);
  return lang ? `${lang.name} / ${lang.nativeName}` : 'English';
};

// Get language codes only
export const getLanguageCodes = () => {
  return languages.map(lang => lang.code);
};

// Languages supported for UI translations (all supported languages)
export const uiLanguages = languages;

export default languages; 