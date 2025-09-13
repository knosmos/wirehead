'use client';
import React, { useState } from "react";

export default function Home() {
  const [inputs, setInputs] = useState(["","",""]);

  const handleInputChange = (index: number, value: string) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);
  };

  const handleAddInput = () => {
    setInputs([...inputs, ""]);
  };

  return (
    <main className="flex min-h-screen flex-col items-center font-mono bg-gray-200">
      <div className="flex min-h-screen flex-col items-center p-24 w-full md:w-1/2">
        <h1 className="text-6xl font-bold my-5 font-serif">Wirehead</h1>
        <p className="uppercase tracking-widest font-mono mb-5">ai for hardware.</p>
        <div className="grid grid-cols-2 w-full gap-4">
          <div className="uppercase tracking-widest font-mono mb-5 text-center">
            <p>list components.</p>
          <div className="rounded-lg border overflow-hidden w-full mt-4">
            {inputs.map((input, idx) => (
              <input
                key={idx}
                type="text"
                value={input}
                onChange={e => handleInputChange(idx, e.target.value)}
                className="px-2 py-2 block border-b w-full bg-gray-100"
                placeholder={`Component ${idx + 1}`}
              />
            ))}
            <button
              type="button"
              onClick={handleAddInput}
              className="px-4 py-2 bg-gray-400 text-white hover:bg-gray-500 w-full cursor-pointer"
            >
              + Add Component
            </button>
          </div>
        </div>
        <div>
          <p className="uppercase tracking-widest font-mono text-center">provide context.</p>
          <textarea
            placeholder="What do you want to build?"
            className="mt-4 px-2 py-1 border rounded-lg w-full h-[calc(100%-3.7rem)] bg-gray-100"
          />
        </div>
        </div>
        <button
          type="button"
          className="mt-4 px-6 py-2 bg-emerald-800 text-white hover:bg-emerald-700 rounded-lg cursor-pointer border border-black w-full"
        >
          Solve for PCB
        </button>
        </div>
    </main>
  );
}
