import { createSlice } from '@reduxjs/toolkit';

const settingsSlice = createSlice({
  name: 'settings',
  initialState: {
    // Accessibility Settings
    fontSize: 'medium', // small, medium, large, xlarge
    highContrast: false,
    reduceMotion: false,
    soundEnabled: true,
    hapticFeedback: true,
    voiceOverEnabled: false,
    
    // Visual Settings
    theme: 'light', // light, dark, auto
    colorScheme: 'default', // default, highContrast, colorBlind
    backgroundStyle: 'default', // default, seasons, elegant, minimal
    
    // Game Settings
    autoSave: true,
    showTimer: true,
    showHints: true,
    confirmActions: true,
    difficulty: 'auto', // easy, medium, hard, auto
    
    // Audio Settings
    musicVolume: 0.7,
    soundVolume: 0.8,
    voiceVolume: 0.9,
    
    // Language Settings
    language: 'bg', // bg, en
    region: 'BG',
    
    // Privacy Settings
    analyticsEnabled: true,
    crashReportingEnabled: true,
    personalizedAds: false,
    
    // Notification Settings
    dailyReminder: true,
    weeklyReport: true,
    achievementNotifications: true,
    soundNotifications: true,
    
    // Performance Settings
    lowPowerMode: false,
    dataSaver: false,
    offlineMode: false
  },
  reducers: {
    // Accessibility Settings
    setFontSize: (state, action) => {
      state.fontSize = action.payload;
    },
    
    toggleHighContrast: (state) => {
      state.highContrast = !state.highContrast;
    },
    
    toggleReduceMotion: (state) => {
      state.reduceMotion = !state.reduceMotion;
    },
    
    toggleSound: (state) => {
      state.soundEnabled = !state.soundEnabled;
    },
    
    toggleHapticFeedback: (state) => {
      state.hapticFeedback = !state.hapticFeedback;
    },
    
    toggleVoiceOver: (state) => {
      state.voiceOverEnabled = !state.voiceOverEnabled;
    },
    
    // Visual Settings
    setTheme: (state, action) => {
      state.theme = action.payload;
    },
    
    setColorScheme: (state, action) => {
      state.colorScheme = action.payload;
    },
    
    setBackgroundStyle: (state, action) => {
      state.backgroundStyle = action.payload;
    },
    
    // Game Settings
    toggleAutoSave: (state) => {
      state.autoSave = !state.autoSave;
    },
    
    toggleShowTimer: (state) => {
      state.showTimer = !state.showTimer;
    },
    
    toggleShowHints: (state) => {
      state.showHints = !state.showHints;
    },
    
    toggleConfirmActions: (state) => {
      state.confirmActions = !state.confirmActions;
    },
    
    setDifficulty: (state, action) => {
      state.difficulty = action.payload;
    },
    
    // Audio Settings
    setMusicVolume: (state, action) => {
      state.musicVolume = Math.max(0, Math.min(1, action.payload));
    },
    
    setSoundVolume: (state, action) => {
      state.soundVolume = Math.max(0, Math.min(1, action.payload));
    },
    
    setVoiceVolume: (state, action) => {
      state.voiceVolume = Math.max(0, Math.min(1, action.payload));
    },
    
    // Language Settings
    setLanguage: (state, action) => {
      state.language = action.payload;
    },
    
    setRegion: (state, action) => {
      state.region = action.payload;
    },
    
    // Privacy Settings
    toggleAnalytics: (state) => {
      state.analyticsEnabled = !state.analyticsEnabled;
    },
    
    toggleCrashReporting: (state) => {
      state.crashReportingEnabled = !state.crashReportingEnabled;
    },
    
    togglePersonalizedAds: (state) => {
      state.personalizedAds = !state.personalizedAds;
    },
    
    // Notification Settings
    toggleDailyReminder: (state) => {
      state.dailyReminder = !state.dailyReminder;
    },
    
    toggleWeeklyReport: (state) => {
      state.weeklyReport = !state.weeklyReport;
    },
    
    toggleAchievementNotifications: (state) => {
      state.achievementNotifications = !state.achievementNotifications;
    },
    
    toggleSoundNotifications: (state) => {
      state.soundNotifications = !state.soundNotifications;
    },
    
    // Performance Settings
    toggleLowPowerMode: (state) => {
      state.lowPowerMode = !state.lowPowerMode;
    },
    
    toggleDataSaver: (state) => {
      state.dataSaver = !state.dataSaver;
    },
    
    toggleOfflineMode: (state) => {
      state.offlineMode = !state.offlineMode;
    },
    
    // Reset to defaults
    resetToDefaults: (state) => {
      return {
        fontSize: 'medium',
        highContrast: false,
        reduceMotion: false,
        soundEnabled: true,
        hapticFeedback: true,
        voiceOverEnabled: false,
        theme: 'light',
        colorScheme: 'default',
        backgroundStyle: 'default',
        autoSave: true,
        showTimer: true,
        showHints: true,
        confirmActions: true,
        difficulty: 'auto',
        musicVolume: 0.7,
        soundVolume: 0.8,
        voiceVolume: 0.9,
        language: 'bg',
        region: 'BG',
        analyticsEnabled: true,
        crashReportingEnabled: true,
        personalizedAds: false,
        dailyReminder: true,
        weeklyReport: true,
        achievementNotifications: true,
        soundNotifications: true,
        lowPowerMode: false,
        dataSaver: false,
        offlineMode: false
      };
    }
  }
});

export const {
  setFontSize,
  toggleHighContrast,
  toggleReduceMotion,
  toggleSound,
  toggleHapticFeedback,
  toggleVoiceOver,
  setTheme,
  setColorScheme,
  setBackgroundStyle,
  toggleAutoSave,
  toggleShowTimer,
  toggleShowHints,
  toggleConfirmActions,
  setDifficulty,
  setMusicVolume,
  setSoundVolume,
  setVoiceVolume,
  setLanguage,
  setRegion,
  toggleAnalytics,
  toggleCrashReporting,
  togglePersonalizedAds,
  toggleDailyReminder,
  toggleWeeklyReport,
  toggleAchievementNotifications,
  toggleSoundNotifications,
  toggleLowPowerMode,
  toggleDataSaver,
  toggleOfflineMode,
  resetToDefaults
} = settingsSlice.actions;

export default settingsSlice.reducer; 