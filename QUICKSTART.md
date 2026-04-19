# Quick Start Guide - LULC Recognition Dashboard

Get the system up and running in 5 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.9+)
python --version

# Check Node version (need 18+)
node --version

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install pnpm (Node package manager)
npm install -g pnpm
```

## Option 1: Using Docker (Easiest)

```bash
# Clone/navigate to project directory
cd lulc-dashboard

# Run both backend and frontend with one command
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Option 2: Manual Setup (Two Terminals)

### Terminal 1 - Backend

```bash
cd backend
uv sync
# Place your trained models in backend/models/:
# - eurosat.pth
# - mrlnset.pth
# - patternnet.pth
uv run app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend

```bash
pnpm install
pnpm dev
```

You should see:
```
  ▲ Next.js 15.x.x
  - Local: http://localhost:3000
```

## Access the Dashboard

1. **Open browser**: http://localhost:3000
2. **See the UI**: Dark theme with indigo accents
3. **Try it out**:
   - Select a dataset (EuroSAT, MLRSNet, or PatternNet)
   - Drag & drop an image or click to upload
   - Click "Run Inference"
   - See predictions with confidence scores

## Test the API Directly

```bash
# In a third terminal
cd backend
python demo_client.py
```

This will:
- Check backend health
- Get system information
- Run predictions on all three models
- Show timings and results

## Using Your Own Models

Once you're ready to use your trained models:

1. **Copy your trained models**:
   ```bash
   cp path/to/your/eurosat_model.pth backend/models/eurosat_fold4.pth
   cp path/to/your/mlrsnet_model.pth backend/models/mlrsnet_fold3.pth
   cp path/to/your/patternnet_model.pth backend/models/patternnet_fold3.pth
   ```

2. **Restart backend**:
   ```bash
   uv run app.py
   ```

3. **That's it!** The frontend will automatically use your models.

## Verify Installation

### Backend Health Check
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "device": "cpu",
  "models_available": ["mlrsnet", "patternnet", "eurosat"]
}
```

### Remote API Test (Production)
```bash
curl https://lulc-recognition-lulc-backend.hf.space/health
```

### System Information
```bash
curl http://localhost:8000/info
```

Should return specifications including:
```json
{
  "architecture": "Explainable CNN",
  "parameters_approx": 400000,
  "flops_approx": 106000000
}
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `Port 8000 already in use` | Change backend port or kill process: `lsof -i :8000` |
| `Port 3000 already in use` | Change frontend port: `pnpm dev -- -p 3001` |
| `Module not found` | Run `uv sync` (backend) or `pnpm install` (frontend) |
| `Models not found` | Run `uv run create_mock_models.py` in backend directory |
| `CORS error` | Ensure frontend and backend URLs match in `.env.local` |
| `GPU not detected` | Set `CUDA_VISIBLE_DEVICES=""` before running backend |

## Development Workflow

### Making Backend Changes
1. Edit Python files in `backend/`
2. Backend auto-reloads with uvicorn (if using hot reload)
3. Or stop and restart: `uv run app.py`

### Making Frontend Changes
1. Edit React components in `components/` or `app/`
2. Changes auto-reload in browser (Next.js HMR)
3. No restart needed!

### Adding New Datasets
1. Add class mappings in `backend/class_mappings.py`
2. Add model config in `backend/model_loader.py`
3. Update UI in `components/DatasetSelector.tsx`

- **Explainability**: Integrated GradCAM, GradCAM++, Saliency, and LIME maps
- **Smart Preprocessing**: Dynamic 64x64 resizing for EuroSAT (skips resize if image <= 64x64)
- **Use GPU**: Automatically detected, speeds up ~3-5x
- **Batch predictions**: Modify backend to accept multiple images

## Documentation

- **Full setup**: See `SETUP.md`
- **Architecture details**: See `README.md`
- **Backend API**: http://localhost:8000/docs (Swagger)
- **Backend code**: See `backend/README.md`
- **Component code**: Check comments in `components/*.tsx`

## Next Steps

1. **Test with sample images**:
   - Find satellite images online
   - Use your own remote sensing images
   - Test different datasets

2. **Replace mock models**:
   - Train your own models
   - Load them following the guide above
   - Observe real inference times

3. **Deploy to production**:
   - Build frontend: `pnpm build`
   - Push backend to cloud (Vercel, AWS, etc.)
   - Update `NEXT_PUBLIC_API_URL` in `.env`

4. **Customize appearance**:
   - Edit theme in `app/globals.css`
   - Modify component styles in `components/*.tsx`
   - Add your branding

## Support

- Check `SETUP.md` for detailed configuration
- Review `backend/README.md` for API details
- Check component source code for implementation details
- See `backend/demo_client.py` for API usage examples

## Success Checklist

- [ ] Backend running (Terminal 1)
- [ ] Frontend running (Terminal 2)
- [ ] Can access http://localhost:3000
- [ ] Can upload an image
- [ ] Prediction works and shows results
- [ ] Can see confidence scores
- [ ] Can switch between datasets

You're all set! Start exploring the LULC Recognition Dashboard.
