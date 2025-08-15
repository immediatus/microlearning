/**
 * Design System for MicroLearning Platform
 * 
 * Centralized design tokens, spacing, typography, and colors
 * optimized for 12-15 year old students on mobile devices
 */

// Color Palette
export const Colors = {
  // Primary Colors
  primary: {
    blue: '#2E86AB',
    teal: '#4ECDC4', 
    orange: '#FFA726',
    red: '#FF6B6B',
  },
  
  // Neutral Colors
  neutral: {
    backgroundLight: '#FAFAFA',
    backgroundDark: '#1A1A1A',
    textPrimary: '#2D2D2D',
    textSecondary: '#757575',
    textInverse: '#FFFFFF',
    border: '#E0E0E0',
    shadow: 'rgba(0, 0, 0, 0.1)',
  },
  
  // Semantic Colors
  semantic: {
    success: '#4CAF50',
    warning: '#FFC107',
    error: '#F44336',
    info: '#2196F3',
  },
  
  // Interactive States
  interactive: {
    correct: '#4ECDC4',
    incorrect: '#FF6B6B',
    pending: '#FFA726',
    disabled: '#BDBDBD',
  },
  
  // Gradients
  gradients: {
    quiz: ['#FF6B6B', '#4ECDC4'],
    progress: ['#2E86AB', '#4ECDC4'],
    achievement: ['#FFA726', '#FF6B6B'],
  },
} as const;

// Typography Scale (responsive for mobile)
export const Typography = {
  // Mobile Typography - scales with device size
  mobile: {
    hero: {
      fontSize: 32,
      fontWeight: '700' as const,
      lineHeight: 40,
      letterSpacing: -0.5,
    },
    h1: {
      fontSize: 28,
      fontWeight: '600' as const,
      lineHeight: 36,
      letterSpacing: -0.25,
    },
    h2: {
      fontSize: 24,
      fontWeight: '600' as const,
      lineHeight: 32,
      letterSpacing: 0,
    },
    h3: {
      fontSize: 20,
      fontWeight: '600' as const,
      lineHeight: 28,
      letterSpacing: 0,
    },
    body: {
      fontSize: 16,
      fontWeight: '400' as const,
      lineHeight: 24,
      letterSpacing: 0,
    },
    bodyLarge: {
      fontSize: 18,
      fontWeight: '400' as const,
      lineHeight: 26,
      letterSpacing: 0,
    },
    caption: {
      fontSize: 14,
      fontWeight: '400' as const,
      lineHeight: 20,
      letterSpacing: 0.25,
    },
    small: {
      fontSize: 12,
      fontWeight: '400' as const,
      lineHeight: 16,
      letterSpacing: 0.4,
    },
  },
  
  // Font weights
  weights: {
    light: '300',
    regular: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  } as const,
} as const;

// Spacing Scale (8px base unit)
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
  xxxl: 64,
} as const;

// Border Radius
export const BorderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  xxl: 24,
  round: 9999,
} as const;

// Shadow Elevations
export const Shadows = {
  none: {
    shadowOpacity: 0,
  },
  sm: {
    shadowColor: Colors.neutral.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: Colors.neutral.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2.22,
    elevation: 3,
  },
  lg: {
    shadowColor: Colors.neutral.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 8,
  },
  xl: {
    shadowColor: Colors.neutral.shadow,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.37,
    shadowRadius: 7.49,
    elevation: 12,
  },
} as const;

// Age-Specific Design Variants
export const AgeGroups = {
  '5-8': {
    touchTargetSize: 60,
    fontSize: 1.2, // 20% larger
    spacing: 1.5, // 50% more spacing
    animationDuration: 600, // Slower animations
    colors: {
      primary: Colors.primary.orange, // More playful
      accent: Colors.primary.teal,
    },
  },
  '9-11': {
    touchTargetSize: 50,
    fontSize: 1.1, // 10% larger
    spacing: 1.25, // 25% more spacing
    animationDuration: 400,
    colors: {
      primary: Colors.primary.teal,
      accent: Colors.primary.blue,
    },
  },
  '12-15': {
    touchTargetSize: 44, // Standard iOS guideline
    fontSize: 1.0, // Base size
    spacing: 1.0, // Base spacing
    animationDuration: 300,
    colors: {
      primary: Colors.primary.blue,
      accent: Colors.primary.teal,
    },
  },
} as const;

// Animation Timings
export const Animations = {
  duration: {
    fast: 150,
    normal: 300,
    slow: 500,
  },
  easing: {
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const;

// Breakpoints for responsive design
export const Breakpoints = {
  phone: 0,
  tablet: 768,
  desktop: 1024,
} as const;

// Z-Index Scale
export const ZIndex = {
  hide: -1,
  base: 0,
  docked: 10,
  dropdown: 1000,
  sticky: 1100,
  banner: 1200,
  overlay: 1300,
  modal: 1400,
  popover: 1500,
  skipLink: 1600,
  toast: 1700,
  tooltip: 1800,
} as const;

// Icon Sizes
export const IconSizes = {
  xs: 12,
  sm: 16,
  md: 20,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

// Component Variants
export const ComponentVariants = {
  button: {
    sizes: {
      sm: {
        paddingVertical: Spacing.sm,
        paddingHorizontal: Spacing.md,
        fontSize: Typography.mobile.caption.fontSize,
        borderRadius: BorderRadius.md,
      },
      md: {
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.lg,
        fontSize: Typography.mobile.body.fontSize,
        borderRadius: BorderRadius.lg,
      },
      lg: {
        paddingVertical: Spacing.lg,
        paddingHorizontal: Spacing.xl,
        fontSize: Typography.mobile.bodyLarge.fontSize,
        borderRadius: BorderRadius.xl,
      },
    },
    variants: {
      primary: {
        backgroundColor: Colors.primary.blue,
        color: Colors.neutral.textInverse,
      },
      secondary: {
        backgroundColor: Colors.primary.teal,
        color: Colors.neutral.textInverse,
      },
      outline: {
        backgroundColor: 'transparent',
        borderWidth: 2,
        borderColor: Colors.primary.blue,
        color: Colors.primary.blue,
      },
      ghost: {
        backgroundColor: 'transparent',
        color: Colors.primary.blue,
      },
    },
  },
  
  card: {
    variants: {
      default: {
        backgroundColor: Colors.neutral.backgroundLight,
        borderRadius: BorderRadius.lg,
        padding: Spacing.md,
        ...Shadows.md,
      },
      elevated: {
        backgroundColor: Colors.neutral.backgroundLight,
        borderRadius: BorderRadius.xl,
        padding: Spacing.lg,
        ...Shadows.lg,
      },
      flat: {
        backgroundColor: Colors.neutral.backgroundLight,
        borderRadius: BorderRadius.lg,
        padding: Spacing.md,
        borderWidth: 1,
        borderColor: Colors.neutral.border,
      },
    },
  },
} as const;

// Accessibility
export const Accessibility = {
  minimumTouchTarget: 44,
  colorContrastRatio: {
    normal: 4.5,
    large: 3.0,
  },
  focusRingWidth: 2,
  focusRingColor: Colors.primary.blue,
} as const;

// Export type definitions
export type ColorScheme = typeof Colors;
export type TypographyScale = typeof Typography;
export type SpacingScale = typeof Spacing;
export type AgeGroup = keyof typeof AgeGroups;