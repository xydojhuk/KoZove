export function toMontenegroE164(input: string): string | null {
  let digits = input.replace(/\D/g, '')

  if (digits.startsWith('00382')) {
    digits = digits.slice(5)
  } else if (digits.startsWith('382')) {
    digits = digits.slice(3)
  }

  if (digits.startsWith('0')) {
    digits = digits.slice(1)
  }

  if (!/^\d{7,9}$/.test(digits)) {
    return null
  }

  return `+382${digits}`
}


export function localMontenegroDigits(full: string): string {
  const digits = full.replace(/\D/g, '')

  return digits.startsWith('382')
    ? digits.slice(3)
    : digits.replace(/^0/, '')
}
