(function(w){
  w.dataLayer = [];

  if(w && w.consentPolicyManager && w.consentPolicyManager.initRan){
      const { policy } = consentPolicyManager.getCurrentConsentPolicy();
      setConsent('default', policy);
  } else {
      setConsent('default', { advertising: false, analytics: false, functional: false, waitForUpdate: 500 });
  }

  w.document.addEventListener("consentPolicyInitialized", ({ detail }) => {
      setConsent('update', detail.policy)
  });

  w.document.addEventListener("consentPolicyChanged", ({ detail }) => {
      setConsent('update', detail.policy)
  });

  function setConsent(action, { advertising, waitForUpdate }) {
      (function() {
          w.dataLayer.push(arguments);
      })('consent', action, {
          'ad_storage': advertising ? 'granted' : 'denied',
          'ad_user_data': advertising ? 'granted' : 'denied',
          'ad_personalization': advertising ? 'granted' : 'denied',
          'analytics_storage': advertising ? 'granted' : 'denied',
          'functionality_storage': advertising ? 'granted' : 'denied',
          'personalization_storage': 'granted',
          'security_storage': 'granted',
          ...waitForUpdate ? { 'wait_for_update': waitForUpdate } : {}
      });
  }

  (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-MDD5C4');
})(globalThis);
