import { forwardRef } from 'react'
import clsx from 'clsx'

const RacingInput = forwardRef(({
  label,
  error,
  className,
  containerClassName,
  ...props
}, ref) => {
  return (
    <div className={clsx('mb-4', containerClassName)}>
      {label && (
        <label className="block font-orbitron font-semibold text-xs uppercase tracking-wide text-chrome-silver mb-2">
          {label}
          {props.required && <span className="text-racing-red ml-1">*</span>}
        </label>
      )}

      <input
        ref={ref}
        className={clsx(
          'racing-input w-full',
          error && 'border-status-danger border-l-status-danger',
          className
        )}
        {...props}
      />

      {error && (
        <p className="mt-1 text-sm text-status-danger font-rajdhani">{error}</p>
      )}
    </div>
  )
})

RacingInput.displayName = 'RacingInput'

export default RacingInput
