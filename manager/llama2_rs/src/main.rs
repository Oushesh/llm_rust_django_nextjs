//import to read in files:
use std::fs::File;
use std::io::{Read,Seek,SeekFrom};
use std::mem::size_of;
use std::path::Path;
use std::os::unix::io::AsRawFd;
use memmap::{Mmap,Protection};

#[derive(Debug)]
struct Config {
    dim: usize,
    hidden_dim: usize,
    n_layers: usize,
    n_heads: usize,
    n_kv_heads: usize,
    vocab_size: usize,
    seq_len: usize,
}

#[derive(Debug)]
struct RunState {
    x: Vec<f32>,
    xb: Vec<f32>,
    xb2: Vec<f32>,
    hb: Vec<f32>,
    hb2: Vec<f32>,
    q: Vec<f32>,
    k: Vec<f32>,
    v: Vec<f32>,
    att: Vec<f32>,
    logits: Vec<f32>,
    key_cache: Vec<f32>,
    value_cache: Vec<f32>,
}

#[derive(Debug)]
struct TransformerWeights {
    token_embedding_table: Vec<f32>,
    rms_att_weight: Vec<f32>,
    rms_ffn_weight: Vec<f32>,
    wq: Vec<f32>,
    wk: Vec<f32>,
    wv: Vec<f32>,
    wo: Vec<f32>,
    w1: Vec<f32>,
    w2: Vec<f32>,
    w3: Vec<f32>,
    rms_final_weight: Vec<f32>,
    wcls: Vec<f32>,
}

#[derive(Debug)]
struct Transformer {
    config: Config,
    weights: TransformerWeights,
    state: RunState,
    file_size: usize,
}

impl RunState {
    fn new(config: &Config) -> RunState {
        let kv_dim = (config.dim * config.n_kv_heads) / config.n_heads;
        RunState {
            x: vec![0.0; config.dim],
            xb: vec![0.0; config.dim],
            xb2: vec![0.0; config.dim],
            hb: vec![0.0; config.hidden_dim],
            hb2: vec![0.0; config.hidden_dim],
            q: vec![0.0; config.dim],
            k: vec![0.0; kv_dim],
            v: vec![0.0; kv_dim],
            att: vec![0.0; config.n_heads * config.seq_len],
            logits: vec![0.0; config.vocab_size],
            key_cache: vec![0.0; config.n_layers * config.seq_len * kv_dim],
            value_cache: vec![0.0; config.n_layers * config.seq_len * kv_dim],
        }
    }
}
//Read the File from checkpoint path:

fn read_checkpoint(
    checkpoint: &Path,
    config: &mut Config,
    weights: &mut TransformerWeights,
)-> Result<(), Box<dyn std::error::Error>>
{
    let mut file = File::open(checkpoint)?;

    // Read in the Config header
    let config_bytes: &mut[u8] = unsafe{
        std::slice::from_raw_parts_mut(
            (config as *mut Config) as *mut u8,
            size_of::<Config>(),
        )
    };
    file.read_exact(config_bytes)?;

    // Use absolute value of vocab_size to
    // determine if weights are shared
    let shared_weights = config.vocab_size.abs();

    // Move file pointer to end of file to figure out the file size
    let file_size = file.seek(SeekFrom::End(0))?;

    // Memory map the Transformer weights into the
    // data pointer
    let mmap = unsafe { Mmap::open_with_offset(&file, Protection::Read, size_of::<Config>(), (file_size - size_of::<Config>() as u64))? };
    let data = mmap.ptr();

    // Set up weights
    // Set up weights
    let weights_ptr: *const f32 = unsafe { data.add(size_of::<Config>()).cast() };
    memory_map_weights(weights, config, weights_ptr, shared_weights > 0);
    Ok(())
}

fn main() {
    let config = Config {
        dim: 512,
        hidden_dim: 2048,
        n_layers: 12,
        n_heads: 8,
        n_kv_heads: 8,
        vocab_size: 256,
        seq_len: 512,
    };

    let run_state = RunState::new(&config);
    let fake_file_data: Vec<f32> = vec![0.0; 1000000];
    let weights = TransformerWeights {
        token_embedding_table: vec![],
        rms_att_weight: vec![],
        rms_ffn_weight: vec![],
        wq: vec![],
        wk: vec![],
        wv: vec![],
        wo: vec![],
        w1: vec![],
        w2: vec![],
        w3: vec![],
        rms_final_weight: vec![],
        wcls: vec![],
    };

    let transformer = Transformer {
        config,
        weights,
        state: run_state,
        file_size: fake_file_data.len() * std::mem::size_of::<f32>(),
    };

    //println!("Transformer object: {:?}", transformer);
    let checkpoint_path = Path::new("");
}
