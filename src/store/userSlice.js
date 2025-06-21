import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { UserService } from '../services/UserService';

export const loadUserProfile = createAsyncThunk(
  'user/loadProfile',
  async (userId) => {
    const profile = await UserService.getProfile(userId);
    return profile;
  }
);

export const updateUserStats = createAsyncThunk(
  'user/updateStats',
  async ({ userId, gameResult }, { getState }) => {
    const { user } = getState();
    const updatedStats = await UserService.updateStats(userId, gameResult);
    return updatedStats;
  }
);

export const unlockAchievement = createAsyncThunk(
  'user/unlockAchievement',
  async ({ userId, achievementType, achievementData }) => {
    const achievement = await UserService.unlockAchievement(userId, achievementType, achievementData);
    return achievement;
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    id: null,
    username: '',
    email: '',
    profile: {
      totalPoints: 0,
      level: 1,
      gamesPlayed: 0,
      gamesCompleted: 0,
      totalTimePlayed: 0,
      averageAccuracy: 0,
      averageTime: 0,
      currentStreak: 0,
      longestStreak: 0,
      favoriteTheme: 'nature'
    },
    achievements: [],
    unlockedThemes: ['nature'],
    unlockedFonts: ['default'],
    unlockedBackgrounds: ['default'],
    dailyLoginStreak: 0,
    lastLoginDate: null,
    loading: false,
    error: null
  },
  reducers: {
    setUser: (state, action) => {
      const { id, username, email } = action.payload;
      state.id = id;
      state.username = username;
      state.email = email;
    },
    
    addPoints: (state, action) => {
      state.profile.totalPoints += action.payload;
      
      // Level up logic
      const newLevel = Math.floor(state.profile.totalPoints / 1000) + 1;
      if (newLevel > state.profile.level) {
        state.profile.level = newLevel;
      }
    },
    
    incrementGamesPlayed: (state) => {
      state.profile.gamesPlayed++;
    },
    
    incrementGamesCompleted: (state) => {
      state.profile.gamesCompleted++;
    },
    
    updateTimePlayed: (state, action) => {
      state.profile.totalTimePlayed += action.payload;
    },
    
    updateAccuracy: (state, action) => {
      const { accuracy, timeSpent } = action.payload;
      const currentTotal = state.profile.averageAccuracy * state.profile.gamesCompleted;
      const newTotal = currentTotal + accuracy;
      state.profile.averageAccuracy = newTotal / (state.profile.gamesCompleted + 1);
      
      const currentTimeTotal = state.profile.averageTime * state.profile.gamesCompleted;
      const newTimeTotal = currentTimeTotal + timeSpent;
      state.profile.averageTime = newTimeTotal / (state.profile.gamesCompleted + 1);
    },
    
    updateStreak: (state, action) => {
      const { completed } = action.payload;
      if (completed) {
        state.profile.currentStreak++;
        if (state.profile.currentStreak > state.profile.longestStreak) {
          state.profile.longestStreak = state.profile.currentStreak;
        }
      } else {
        state.profile.currentStreak = 0;
      }
    },
    
    unlockTheme: (state, action) => {
      const theme = action.payload;
      if (!state.unlockedThemes.includes(theme)) {
        state.unlockedThemes.push(theme);
      }
    },
    
    unlockFont: (state, action) => {
      const font = action.payload;
      if (!state.unlockedFonts.includes(font)) {
        state.unlockedFonts.push(font);
      }
    },
    
    unlockBackground: (state, action) => {
      const background = action.payload;
      if (!state.unlockedBackgrounds.includes(background)) {
        state.unlockedBackgrounds.push(background);
      }
    },
    
    updateDailyLogin: (state) => {
      const today = new Date().toDateString();
      const lastLogin = state.lastLoginDate ? new Date(state.lastLoginDate).toDateString() : null;
      
      if (lastLogin !== today) {
        if (lastLogin === new Date(Date.now() - 24 * 60 * 60 * 1000).toDateString()) {
          state.dailyLoginStreak++;
        } else {
          state.dailyLoginStreak = 1;
        }
        state.lastLoginDate = new Date().toISOString();
      }
    },
    
    setFavoriteTheme: (state, action) => {
      state.profile.favoriteTheme = action.payload;
    },
    
    clearUser: (state) => {
      state.id = null;
      state.username = '';
      state.email = '';
      state.profile = {
        totalPoints: 0,
        level: 1,
        gamesPlayed: 0,
        gamesCompleted: 0,
        totalTimePlayed: 0,
        averageAccuracy: 0,
        averageTime: 0,
        currentStreak: 0,
        longestStreak: 0,
        favoriteTheme: 'nature'
      };
      state.achievements = [];
      state.unlockedThemes = ['nature'];
      state.unlockedFonts = ['default'];
      state.unlockedBackgrounds = ['default'];
      state.dailyLoginStreak = 0;
      state.lastLoginDate = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadUserProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadUserProfile.fulfilled, (state, action) => {
        state.loading = false;
        Object.assign(state, action.payload);
      })
      .addCase(loadUserProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(updateUserStats.fulfilled, (state, action) => {
        Object.assign(state.profile, action.payload);
      })
      .addCase(unlockAchievement.fulfilled, (state, action) => {
        state.achievements.push(action.payload);
      });
  }
});

export const {
  setUser,
  addPoints,
  incrementGamesPlayed,
  incrementGamesCompleted,
  updateTimePlayed,
  updateAccuracy,
  updateStreak,
  unlockTheme,
  unlockFont,
  unlockBackground,
  updateDailyLogin,
  setFavoriteTheme,
  clearUser
} = userSlice.actions;

export default userSlice.reducer; 