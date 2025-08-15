import * as React from 'react';

const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  ageGroup?: '5-8' | '9-11' | '12-15';
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ageGroup = '9-11', ...props }, ref) => {
    const baseClasses =
      'flex w-full rounded-md border border-gray-300 bg-transparent shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50';

    const ageGroupClasses = {
      '5-8': 'text-lg py-3 px-4 min-h-[48px]',
      '9-11': 'text-base py-2 px-3 min-h-[44px]',
      '12-15': 'text-sm py-2 px-2 min-h-[40px]',
    };

    const finalClasses = cn(
      baseClasses,
      ageGroupClasses[ageGroup],
      className
    );

    return (
      <input
        type={type}
        className={finalClasses}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';

export { Input };
