/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./templates/*.html'],
    theme: {
        extend: {
            colors: {
                'custom-blue': '#153E75',
                'cyber-dark': '#121212',
                'cyber-cyan': '#00FFFF',
                'cyber-purple': '#800080',
                'cyber-pink': '#FF69B4',
                'cyber-red': '#FF0000',
                'cyber-green': '#00FF00',
                'cyber-blue': '#0000FF',
                'cyber-yellow': '#FFFF00',
            },
            'gray-100': '#F3F4F6',
            'gray-200': '#E5E7EB',
            'gray-300': '#D1D5DB',
            'gray-400': '#9CA3AF',
            'gray-500': '#6B7280',
            'gray-600': '#4B5563',
            'gray-700': '#374151',
            'gray-800': '#1F2937',
            'gray-900': '#111827'
        },
    },
    plugins: [require('@tailwindcss/forms')],

}