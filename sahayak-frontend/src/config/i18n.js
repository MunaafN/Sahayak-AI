import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      // Navigation
      'nav.dashboard': 'Dashboard',
      'nav.content': 'Content Generator',
      'nav.worksheets': 'Worksheets',
      'nav.knowledge': 'Knowledge Base',
      'nav.visuals': 'Visual Aids',
      'nav.assessment': 'Reading Assessment',
      'nav.planner': 'Lesson Planner',
      'nav.logout': 'Logout',
      
      // Common
      'common.submit': 'Submit',
      'common.cancel': 'Cancel',
      'common.save': 'Save',
      'common.download': 'Download',
      'common.upload': 'Upload',
      'common.loading': 'Loading...',
      'common.error': 'Error',
      'common.success': 'Success',
      
      // Auth
      'auth.login': 'Login',
      'auth.signup': 'Sign Up',
      'auth.email': 'Email',
      'auth.password': 'Password',
      'auth.welcomeBack': 'Welcome back to Sahayak',
      'auth.createAccount': 'Create your Sahayak account',
      
      // Dashboard
      'dashboard.title': 'Welcome to Sahayak',
      'dashboard.subtitle': 'AI-powered teaching assistant for multi-grade classrooms',
      
      // Modules
      'modules.content.title': 'Hyper-Local Content Generator',
      'modules.content.description': 'Generate stories and content in local languages',
      'modules.worksheets.title': 'Differentiated Worksheet Generator',
      'modules.worksheets.description': 'Create grade-specific worksheets from textbook images',
      'modules.knowledge.title': 'Knowledge Base',
      'modules.knowledge.description': 'Get simple explanations for complex questions',
      'modules.visuals.title': 'Visual Aid Generator',
      'modules.visuals.description': 'Create diagrams and illustrations for teaching',
      'modules.assessment.title': 'Audio-Based Reading Assessment',
      'modules.assessment.description': 'Assess student reading fluency with AI',
      'modules.planner.title': 'AI Lesson Planner',
      'modules.planner.description': 'Generate structured lesson plans for any topic'
    }
  },
  hi: {
    translation: {
      // Navigation
      'nav.dashboard': 'डैशबोर्ड',
      'nav.content': 'सामग्री जेनरेटर',
      'nav.worksheets': 'वर्कशीट',
      'nav.knowledge': 'ज्ञान आधार',
      'nav.visuals': 'दृश्य सहायता',
      'nav.assessment': 'पढ़ने का मूल्यांकन',
      'nav.planner': 'पाठ योजना',
      'nav.logout': 'लॉग आउट',
      
      // Common
      'common.submit': 'जमा करें',
      'common.cancel': 'रद्द करें',
      'common.save': 'सेव करें',
      'common.download': 'डाउनलोड',
      'common.upload': 'अपलोड',
      'common.loading': 'लोड हो रहा है...',
      'common.error': 'त्रुटि',
      'common.success': 'सफलता',
      
      // Auth
      'auth.login': 'लॉग इन',
      'auth.signup': 'साइन अप',
      'auth.email': 'ईमेल',
      'auth.password': 'पासवर्ड',
      'auth.welcomeBack': 'सहायक में वापस स्वागत है',
      'auth.createAccount': 'अपना सहायक खाता बनाएं',
      
      // Dashboard
      'dashboard.title': 'सहायक में स्वागत है',
      'dashboard.subtitle': 'बहु-ग्रेड कक्षाओं के लिए AI-संचालित शिक्षण सहायक',
      
      // Modules
      'modules.content.title': 'स्थानीय सामग्री जेनरेटर',
      'modules.content.description': 'स्थानीय भाषाओं में कहानियां और सामग्री बनाएं',
      'modules.worksheets.title': 'विभेदित वर्कशीट जेनरेटर',
      'modules.worksheets.description': 'पाठ्यपुस्तक चित्रों से ग्रेड-विशिष्ट वर्कशीट बनाएं',
      'modules.knowledge.title': 'ज्ञान आधार',
      'modules.knowledge.description': 'जटिल प्रश्नों के लिए सरल स्पष्टीकरण प्राप्त करें',
      'modules.visuals.title': 'दृश्य सहायता जेनरेटर',
      'modules.visuals.description': 'शिक्षण के लिए आरेख और चित्र बनाएं',
      'modules.assessment.title': 'ऑडियो-आधारित पढ़ने का मूल्यांकन',
      'modules.assessment.description': 'AI के साथ छात्र पढ़ने की धाराप्रवाहता का आकलन करें',
      'modules.planner.title': 'AI पाठ योजनाकार',
      'modules.planner.description': 'किसी भी विषय के लिए संरचित पाठ योजना बनाएं'
    }
  },
  mr: {
    translation: {
      // Navigation
      'nav.dashboard': 'डॅशबोर्ड',
      'nav.content': 'सामग्री जनरेटर',
      'nav.worksheets': 'वर्कशीट',
      'nav.knowledge': 'ज्ञान आधार',
      'nav.visuals': 'दृश्य सहाय्य',
      'nav.assessment': 'वाचन मूल्यांकन',
      'nav.planner': 'धडा योजना',
      'nav.logout': 'लॉग आउट',
      
      // Common
      'common.submit': 'सबमिट करा',
      'common.cancel': 'रद्द करा',
      'common.save': 'जतन करा',
      'common.download': 'डाऊनलोड',
      'common.upload': 'अपलोड',
      'common.loading': 'लोड होत आहे...',
      'common.error': 'त्रुटी',
      'common.success': 'यशस्वी',
      
      // Auth
      'auth.login': 'लॉग इन',
      'auth.signup': 'साइन अप',
      'auth.email': 'ईमेल',
      'auth.password': 'पासवर्ड',
      'auth.welcomeBack': 'सहायकमध्ये परत स्वागत आहे',
      'auth.createAccount': 'तुमचे सहायक खाते तयार करा',
      
      // Dashboard
      'dashboard.title': 'सहायकमध्ये स्वागत आहे',
      'dashboard.subtitle': 'बहु-इयत्ता वर्गांसाठी AI-चालित शिक्षण सहाय्यक',
      
      // Modules
      'modules.content.title': 'स्थानिक सामग्री जनरेटर',
      'modules.content.description': 'स्थानिक भाषांमध्ये कथा आणि सामग्री तयार करा',
      'modules.worksheets.title': 'विभेदित वर्कशीट जनरेटर',
      'modules.worksheets.description': 'पाठ्यपुस्तक प्रतिमांवरून इयत्ता-विशिष्ट वर्कशीट तयार करा',
      'modules.knowledge.title': 'ज्ञान आधार',
      'modules.knowledge.description': 'जटिल प्रश्नांसाठी सोपे स्पष्टीकरण मिळवा',
      'modules.visuals.title': 'दृश्य सहाय्य जनरेटर',
      'modules.visuals.description': 'शिक्षणासाठी आकृत्या आणि चित्रे तयार करा',
      'modules.assessment.title': 'ऑडिओ-आधारित वाचन मूल्यांकन',
      'modules.assessment.description': 'AI सह विद्यार्थी वाचन प्रवाहता चे मूल्यांकन करा',
      'modules.planner.title': 'AI धडा योजनाकार',
      'modules.planner.description': 'कोणत्याही विषयासाठी संरचित धडा योजना तयार करा'
    }
  },
  bn: {
    translation: {
      // Navigation
      'nav.dashboard': 'ড্যাশবোর্ড',
      'nav.content': 'কন্টেন্ট জেনেরেটর',
      'nav.worksheets': 'ওয়ার্কশীট',
      'nav.knowledge': 'জ্ঞানের ভিত্তি',
      'nav.visuals': 'ভিজ্যুয়াল এইড',
      'nav.assessment': 'পড়া মূল্যায়ন',
      'nav.planner': 'পাঠ পরিকল্পনা',
      'nav.logout': 'লগ আউট',
      
      // Dashboard
      'dashboard.title': 'সহায়কে স্বাগতম',
      'dashboard.subtitle': 'বহু-গ্রেড শ্রেণীকক্ষের জন্য AI-চালিত শিক্ষণ সহায়ক'
    }
  },
  te: {
    translation: {
      // Navigation
      'nav.dashboard': 'డాష్‌బోర్డ్',
      'nav.content': 'కంటెంట్ జనరేటర్',
      'nav.worksheets': 'వర్క్‌షీట్‌లు',
      'nav.knowledge': 'జ్ఞాన ఆధారం',
      'nav.visuals': 'దృశ్య సహాయాలు',
      'nav.assessment': 'పఠన మూల్యాంకనం',
      'nav.planner': 'పాఠ ప్రణాళిక',
      'nav.logout': 'లాగ్ అవుట్',
      
      // Dashboard
      'dashboard.title': 'సహాయక్‌కు స్వాగతం',
      'dashboard.subtitle': 'బహుళ-గ్రేడ్ తరగతుల కోసం AI-శక్తితో కూడిన బోధనా సహాయకుడు'
    }
  },
  ta: {
    translation: {
      // Navigation
      'nav.dashboard': 'டாஷ்போர்ட்',
      'nav.content': 'உள்ளடக்க உருவாக்கி',
      'nav.worksheets': 'பணித்தாள்கள்',
      'nav.knowledge': 'அறிவுத் தளம்',
      'nav.visuals': 'காட்சி உதவிகள்',
      'nav.assessment': 'வாசிப்பு மதிப்பீடு',
      'nav.planner': 'பாட திட்டம்',
      'nav.logout': 'வெளியேறு',
      
      // Dashboard
      'dashboard.title': 'சகாயக்கிற்கு வரவேற்கிறோம்',
      'dashboard.subtitle': 'பல்வேறு வகுப்புகளுக்கான AI-இயங்கும் கற்பித்தல் உதவியாளர்'
    }
  },
  gu: {
    translation: {
      // Navigation
      'nav.dashboard': 'ડેશબોર્ડ',
      'nav.content': 'સામગ્રી જનરેટર',
      'nav.worksheets': 'વર્કશીટ',
      'nav.knowledge': 'જ્ઞાન આધાર',
      'nav.visuals': 'દ્રશ્ય સહાય',
      'nav.assessment': 'વાંચન મૂલ્યાંકન',
      'nav.planner': 'પાઠ યોજનાકાર',
      'nav.logout': 'લૉગ આઉટ',
      
      // Dashboard
      'dashboard.title': 'સહાયકમાં સ્વાગત છે',
      'dashboard.subtitle': 'બહુ-ગ્રેડ વર્ગખંડો માટે AI-સંચાલિત શિક્ષણ સહાયક'
    }
  },
  kn: {
    translation: {
      // Navigation
      'nav.dashboard': 'ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
      'nav.content': 'ವಿಷಯ ಉತ್ಪಾದಕ',
      'nav.worksheets': 'ಕಾರ್ಯಪತ್ರಿಕೆಗಳು',
      'nav.knowledge': 'ಜ್ಞಾನ ಆಧಾರ',
      'nav.visuals': 'ದೃಶ್ಯ ಸಹಾಯಗಳು',
      'nav.assessment': 'ಓದುವ ಮೌಲ್ಯಮಾಪನ',
      'nav.planner': 'ಪಾಠ ಯೋಜಕ',
      'nav.logout': 'ಲಾಗ್ ಔಟ್',
      
      // Dashboard
      'dashboard.title': 'ಸಹಾಯಕಕ್ಕೆ ಸ್ವಾಗತ',
      'dashboard.subtitle': 'ಬಹು-ದರ್ಜೆ ತರಗತಿಗಳಿಗೆ AI-ಚಾಲಿತ ಬೋಧನಾ ಸಹಾಯಕ'
    }
  },
  ml: {
    translation: {
      // Navigation
      'nav.dashboard': 'ഡാഷ്ബോർഡ്',
      'nav.content': 'ഉള്ളടക്ക ജനറേറ്റർ',
      'nav.worksheets': 'വർക്ക്ഷീറ്റുകൾ',
      'nav.knowledge': 'അറിവിന്റെ അടിസ്ഥാനം',
      'nav.visuals': 'വിഷ്വൽ സഹായങ്ങൾ',
      'nav.assessment': 'വായനാ വിലയിരുത്തൽ',
      'nav.planner': 'പാഠ ആസൂത്രകൻ',
      'nav.logout': 'ലോഗ് ഔട്ട്',
      
      // Dashboard
      'dashboard.title': 'സഹായക്കിലേക്ക് സ്വാഗതം',
      'dashboard.subtitle': 'മൾട്ടി-ഗ്രേഡ് ക്ലാസ്റൂമുകൾക്കായി AI-പവർഡ് ടീച്ചിംഗ് അസിസ്റ്റന്റ്'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('sahayak_language') || 'en', // Load saved language
    fallbackLng: 'en',
    
    interpolation: {
      escapeValue: false
    }
  });

export default i18n; 