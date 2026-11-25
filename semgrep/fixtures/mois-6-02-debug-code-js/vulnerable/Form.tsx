import React from 'react';

export function Form({ onSubmit }: { onSubmit: (v: string) => void }) {
  const submit = (v: string) => {
    // ruleid: mois-6-02-debug-code-js
    console.debug('submit', v);
    onSubmit(v);
  };
  return <input onBlur={(e) => submit(e.target.value)} />;
}
