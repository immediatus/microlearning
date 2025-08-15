import * as React from 'react';

// A simple utility for conditional class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'destructive' | 'ghost' | 'link';
  ageGroup?: '5-8' | '9-11' | '12-15';
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', ageGroup = '9-11', ...props }, ref) => {
    const baseClasses =
      'inline-flex items-center justify-center font-bold rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed';

    const variantClasses = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
      secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400',
      destructive: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      ghost: 'bg-transparent hover:bg-gray-100 focus:ring-gray-400',
      link: 'bg-transparent text-blue-600 underline hover:text-blue-800 focus:ring-blue-500',
    };

    const ageGroupClasses = {
      '5-8': 'text-lg py-3 px-6 min-h-[48px]',
      '9-11': 'text-base py-2 px-4 min-h-[44px]',
      '12-15': 'text-sm py-2 px-3 min-h-[40px]',
    };

    const finalClasses = cn(
      baseClasses,
      variantClasses[variant],
      ageGroupClasses[ageGroup],
      className
    );

    return <button className={finalClasses} ref={ref} {...props} />;
  }
);

Button.displayName = 'Button';

export { Button };
