// supabaseSync.js – simple OTP sync wrapper using Supabase
import { supabase } from './supabaseClient.js';

// Ensure the table exists (run once). Table: otp_state with columns: id (int PK), expectedOtp (text)
async function ensureTable() {
  const { data, error } = await supabase.from('otp_state').select('*');
  if (error && error.code === '42P01') { // table does not exist
    await supabase.rpc('create_otp_state_table'); // placeholder, assume you have a function or run manually
  }
}

// Set OTP value (or null to clear)
export async function setSync(key, value) {
  // For this project we only sync a single key: expectedOtp
  const { error } = await supabase.from('otp_state').upsert({ id: 1, expectedOtp: value }, { onConflict: 'id' });
  if (error) console.error('Supabase setSync error:', error);
}

// Get OTP value
export async function getSync(key) {
  const { data, error } = await supabase.from('otp_state').select('expectedOtp').eq('id', 1).single();
  if (error) {
    console.error('Supabase getSync error:', error);
    return null;
  }
  return data?.expectedOtp ?? null;
}

// Subscribe to realtime changes (optional – for illustration)
export function subscribeSync(key, callback) {
  supabase
    .from('otp_state:id=eq.1')
    .on('UPDATE', payload => {
      const newVal = payload.new?.expectedOtp;
      callback(newVal);
    })
    .subscribe();
}

// Initialize on load
ensureTable();
