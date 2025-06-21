import { BULGARIAN_WORDS } from '../data/bulgarianWords';

export class BulgarianDictionary {
  static BULGARIAN_ALPHABET = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 
    'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 
    'Ъ', 'Ь', 'Ю', 'Я'
  ];
  
  static validateWord(word) {
    if (!word || typeof word !== 'string') {
      return false;
    }
    
    // Check if word contains only Bulgarian letters
    const bulgarianRegex = /^[А-Я]+$/i;
    if (!bulgarianRegex.test(word)) {
      return false;
    }
    
    // Check if word exists in dictionary
    const normalizedWord = word.toUpperCase();
    return BULGARIAN_WORDS.includes(normalizedWord);
  }
  
  static validateBulgarianInput(text) {
    const bulgarianRegex = /^[А-Я\s]+$/i;
    return bulgarianRegex.test(text);
  }
  
  static getWordDefinition(word) {
    const normalizedWord = word.toUpperCase();
    // This would typically connect to a Bulgarian dictionary API
    // For now, return a simple definition based on word length
    return {
      word: normalizedWord,
      definition: `Българска дума с ${word.length} букви`,
      length: word.length,
      frequency: this.getWordFrequency(normalizedWord)
    };
  }
  
  static getWordFrequency(word) {
    const normalizedWord = word.toUpperCase();
    // Simple frequency calculation based on word length
    // In a real app, this would come from a corpus analysis
    const length = word.length;
    if (length <= 3) return 'high';
    if (length <= 5) return 'medium';
    if (length <= 8) return 'low';
    return 'rare';
  }
  
  static getRandomWord(minLength = 3, maxLength = 10) {
    const filteredWords = BULGARIAN_WORDS.filter(word => 
      word.length >= minLength && word.length <= maxLength
    );
    
    if (filteredWords.length === 0) {
      return null;
    }
    
    const randomIndex = Math.floor(Math.random() * filteredWords.length);
    return filteredWords[randomIndex];
  }
  
  static getWordsByTheme(theme) {
    // Return theme-specific words
    const themeWords = {
      nature: ['ГОРА', 'РЕКА', 'ПЛАНИНА', 'ЦВЕТЕ', 'ДЪРВО', 'ЛИСТО', 'ПТИЦА', 'ЖИВОТНО'],
      cities: ['СОФИЯ', 'ПЛОВДИВ', 'ВАРНА', 'БУРГАС', 'РУСЕ', 'СТАРА ЗАГОРА'],
      food: ['БАНИЦА', 'КЕБАПЧЕ', 'ЛЮТЕНИЦА', 'ТАРАТОР', 'КАВАРМА'],
      proverbs: ['ТЪРПЕНИЕ', 'МЪДРОСТ', 'ДОБРОТА', 'ЧЕСТНОСТ']
    };
    
    return themeWords[theme] || themeWords.nature;
  }
  
  static getWordsByLength(length) {
    return BULGARIAN_WORDS.filter(word => word.length === length);
  }
  
  static getWordsByPattern(pattern) {
    // pattern should be a string with letters and underscores for unknown letters
    // e.g., "К_Т" would match "КАТ", "КУТ", etc.
    const regex = new RegExp('^' + pattern.replace(/_/g, '[А-Я]') + '$');
    return BULGARIAN_WORDS.filter(word => regex.test(word));
  }
  
  static isPalindrome(word) {
    const normalized = word.toUpperCase().replace(/\s/g, '');
    return normalized === normalized.split('').reverse().join('');
  }
  
  static getAnagrams(word) {
    const normalized = word.toUpperCase();
    const sorted = normalized.split('').sort().join('');
    
    return BULGARIAN_WORDS.filter(dictWord => 
      dictWord.split('').sort().join('') === sorted && dictWord !== normalized
    );
  }
  
  static getWordScore(word) {
    // Simple scoring system based on word characteristics
    let score = word.length * 10;
    
    // Bonus for longer words
    if (word.length > 8) score += 20;
    if (word.length > 12) score += 30;
    
    // Bonus for rare letters
    const rareLetters = ['Ж', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ь'];
    const rareCount = word.split('').filter(letter => rareLetters.includes(letter)).length;
    score += rareCount * 5;
    
    // Bonus for palindromes
    if (this.isPalindrome(word)) score += 50;
    
    return score;
  }
  
  static getWordDifficulty(word) {
    const length = word.length;
    const frequency = this.getWordFrequency(word);
    const rareLetters = ['Ж', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ь'];
    const rareCount = word.split('').filter(letter => rareLetters.includes(letter)).length;
    
    let difficulty = 1;
    
    if (length > 8) difficulty++;
    if (length > 12) difficulty++;
    if (frequency === 'rare') difficulty++;
    if (rareCount > 2) difficulty++;
    
    return Math.min(difficulty, 5);
  }
  
  static getWordHints(word, hintLevel = 1) {
    const hints = [];
    const wordLength = word.length;
    
    switch (hintLevel) {
      case 1:
        // Show first and last letter
        hints.push(`Започва с "${word[0]}" и завършва с "${word[wordLength - 1]}"`);
        break;
      case 2:
        // Show first letter and length
        hints.push(`Започва с "${word[0]}" и има ${wordLength} букви`);
        break;
      case 3:
        // Show definition
        hints.push(this.getWordDefinition(word).definition);
        break;
      case 4:
        // Show partial word
        const revealed = Math.ceil(wordLength * 0.3);
        let partialWord = '';
        for (let i = 0; i < wordLength; i++) {
          if (i < revealed || Math.random() < 0.1) {
            partialWord += word[i];
          } else {
            partialWord += '_';
          }
        }
        hints.push(`Подсказка: ${partialWord}`);
        break;
    }
    
    return hints;
  }
} 