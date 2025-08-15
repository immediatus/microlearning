/**
 * Button Component for MicroLearning Web App
 * 
 * Mobile-first button component with touch-optimized interactions
 * and age-adaptive styling for educational content
 */

import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 shadow-md hover:shadow-lg',
        secondary: 'bg-teal-500 text-white hover:bg-teal-600 shadow-md hover:shadow-lg',
        outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50 active:bg-blue-100',
        ghost: 'text-blue-600 hover:bg-blue-50 active:bg-blue-100',
        correct: 'bg-teal-500 text-white hover:bg-teal-600 shadow-md',
        incorrect: 'bg-red-500 text-white hover:bg-red-600 shadow-md',
      },
      size: {
        sm: 'h-10 px-4 text-sm min-w-[44px]', // Minimum touch target
        md: 'h-12 px-6 text-base min-w-[44px]',
        lg: 'h-14 px-8 text-lg min-w-[48px]',
        xl: 'h-16 px-10 text-xl min-w-[56px]', // For quiz buttons
      },
      ageGroup: {
        '5-8': 'text-lg px-8 py-4 min-h-[60px] rounded-xl shadow-lg', // Larger for younger kids
        '9-11': 'text-base px-6 py-3 min-h-[50px] rounded-lg shadow-md',
        '12-15': 'text-base px-6 py-3 min-h-[44px] rounded-lg shadow-md', // Standard
      },
      fullWidth: {
        true: 'w-full',
        false: 'w-auto',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
      ageGroup: '12-15',
      fullWidth: false,
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
  children: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ageGroup, fullWidth, loading, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, ageGroup, fullWidth, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            <span>Loading...</span>
          </div>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

// Specialized button variants for quiz interactions
interface QuizButtonProps extends Omit<ButtonProps, 'variant'> {
  choice: 'yes' | 'no';
  isSelected?: boolean;
  showFeedback?: boolean;
  isCorrect?: boolean;
}

export const QuizButton = React.forwardRef<HTMLButtonElement, QuizButtonProps>(
  ({ choice, isSelected, showFeedback, isCorrect, className, children, ...props }, ref) => {
    const getVariant = () => {
      if (!showFeedback) {
        return choice === 'yes' ? 'secondary' : 'outline';
      }
      
      if (isSelected) {
        return isCorrect ? 'correct' : 'incorrect';
      }
      
      return 'ghost';
    };

    return (
      <Button
        ref={ref}
        variant={getVariant()}
        size="xl"
        fullWidth
        className={cn(
          'transition-all duration-300 transform',
          isSelected && showFeedback && 'ring-4 ring-white ring-opacity-50',
          className
        )}
        {...props}
      >
        {children}
      </Button>
    );
  }
);

QuizButton.displayName = 'QuizButton';

// Binary choice buttons for left/right tap zones
interface BinaryChoiceProps extends Omit<ButtonProps, 'variant'> {
  zone: 'left' | 'right';
  answer: boolean; // true for yes, false for no
  showResult?: boolean;
  isCorrect?: boolean;
}

export const BinaryChoiceButton = React.forwardRef<HTMLButtonElement, BinaryChoiceProps>(
  ({ zone, answer, showResult, isCorrect, className, children, ...props }, ref) => {
    const baseClasses = 'h-32 md:h-40 flex-1 text-2xl font-bold relative overflow-hidden';
    
    const getZoneClasses = () => {
      if (!showResult) {
        return zone === 'left' 
          ? 'bg-red-500 hover:bg-red-600 text-white' 
          : 'bg-teal-500 hover:bg-teal-600 text-white';
      }
      
      // Show result feedback
      if (isCorrect) {
        return 'bg-green-500 text-white animate-pulse';
      } else {
        return 'bg-red-600 text-white opacity-75';
      }
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseClasses,
          getZoneClasses(),
          'transition-all duration-300 active:scale-95 rounded-lg shadow-lg',
          'focus:outline-none focus:ring-4 focus:ring-white focus:ring-opacity-50',
          className
        )}
        {...props}
      >
        <div className="relative z-10 flex items-center justify-center h-full">
          {children}
        </div>
        
        {/* Ripple effect on tap */}
        <div className="absolute inset-0 bg-white opacity-0 transition-opacity duration-200 active:opacity-20" />
      </button>
    );
  }
);

BinaryChoiceButton.displayName = 'BinaryChoiceButton';

// Floating action button for video controls
interface FloatingButtonProps extends Omit<ButtonProps, 'variant' | 'size'> {
  icon: React.ReactNode;
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
}

export const FloatingButton = React.forwardRef<HTMLButtonElement, FloatingButtonProps>(
  ({ icon, position = 'bottom-right', className, ...props }, ref) => {
    const positionClasses = {
      'bottom-right': 'fixed bottom-6 right-6',
      'bottom-left': 'fixed bottom-6 left-6',
      'top-right': 'fixed top-6 right-6',
      'top-left': 'fixed top-6 left-6',
    };

    return (
      <Button
        ref={ref}
        variant="primary"
        size="lg"
        className={cn(
          'rounded-full w-14 h-14 p-0 shadow-lg hover:shadow-xl z-50',
          positionClasses[position],
          className
        )}
        {...props}
      >
        {icon}
      </Button>
    );
  }
);

FloatingButton.displayName = 'FloatingButton';