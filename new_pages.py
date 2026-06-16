
# Ensure timedelta is available
from datetime import timedelta

# Hourly Forecast Page
def render_hourly_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">⏰ 24-Hour Hourly Forecast</h1>
            <p class="page-subtitle">Detailed hourly predictions with interactive visualizations for comprehensive planning</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    # Auto-generate hourly forecast for today and display Temperature by default (like AccuWeather)
    sel_date = date.today()
    with st.spinner("⏳ Generating 24-hour forecast for today..."):
        df_hourly = generate_hourly_forecast(models, scalers, features, metadata, sel_date)

    st.markdown(f"<h3 style='color: #f59e0b; text-align: center;'>{sel_date.strftime('%A, %B %d, %Y')} - Hourly Predictions (Default: Temperature)</h3>", unsafe_allow_html=True)

    # Show default Temperature line plot
    default_param = 'T2M' if 'T2M' in metadata else list(metadata.keys())[0]
    # Show textual hourly temperatures first (1 AM - 12 PM)
    st.markdown("### 🌡️ Hourly Temperatures (1 AM - 12 AM)")
    temp_param = default_param
    for h in range(1, 25):
        hour24 = h % 24
        hour_label = f"{hour24:02d}:00"
        row = df_hourly[df_hourly['Hour'] == hour_label]
        if not row.empty:
            val = float(row.iloc[0][temp_param])
            # simple emoji mapping for temperature ranges
            if val < 10:
                e = '❄️'
            elif val < 20:
                e = '🧊'
            elif val < 30:
                e = '☀️'
            else:
                e = '🔥'
            ampm = 'AM' if hour24 < 12 else 'PM'
            display_hour = hour24 % 12
            if display_hour == 0:
                display_hour = 12
            unit = metadata.get(temp_param, {}).get('unit', '')
            st.markdown(f"- **{display_hour} {ampm}** — {val:.1f} {unit} {e}")

    # Then show default Temperature line plot
    fig = create_hourly_line_plot(df_hourly, metadata, default_param, f"({sel_date.strftime('%b %d')})")
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key="hourly_plot_default")

    # Provide optional controls for advanced users
    with st.expander("Options: change parameter, plot type, or export data", expanded=False):
        param_col1, param_col2 = st.columns([2, 1])
        with param_col1:
            selected_target = st.selectbox("🎯 Select Parameter to Visualize", options=list(metadata.keys()), index=list(metadata.keys()).index(default_param), key="hourly_param")
        with param_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            plot_type = st.selectbox("📊 Plot Type", options=['Line Plot', 'Multi-Parameter', 'Heatmap'], key="hourly_plot")

        if plot_type == 'Line Plot':
            fig2 = create_hourly_line_plot(df_hourly, metadata, selected_target, f"({sel_date.strftime('%b %d')})")
            if fig2:
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True}, key="hourly_plot_selected")
        elif plot_type == 'Multi-Parameter':
            multi_params = st.multiselect("Select Multiple Parameters", options=list(metadata.keys()), default=['T2M', 'RH2M', 'WS10M'], key="hourly_multi")
            if multi_params:
                fig = create_multi_line_plot(df_hourly, multi_params, metadata)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key="hourly_plot_multi")
        elif plot_type == 'Heatmap':
            heatmap_params = st.multiselect("Select Parameters for Heatmap", options=list(metadata.keys()), default=['T2M', 'RH2M', 'PRECTOTCORR', 'WS10M'], key="hourly_heatmap")
            if heatmap_params:
                fig = create_heatmap_hourly(df_hourly, heatmap_params, metadata)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key="hourly_plot_heatmap")

        if st.checkbox("📋 Show Detailed Data Table", key="hourly_table"):
            st.dataframe(df_hourly, use_container_width=True)

        # Quick export
        st.markdown("---")
        st.markdown("### 💾 Quick Export")
        export_summary = generate_export_summary(df_hourly, list(metadata.keys())[:5])
        create_quick_export_button(export_summary, f"hourly_forecast_{sel_date.strftime('%Y%m%d')}")

        csv = df_hourly.to_csv(index=False)
        st.download_button("📥 Download Hourly Data (CSV)", data=csv, file_name=f"hourly_forecast_{sel_date.strftime('%Y%m%d')}.csv", mime="text/csv", key="hourly_download")

# Weekly Forecast Page
def render_weekly_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">📅 7-Day Weekly Forecast</h1>
            <p class="page-subtitle">Week-long forecast with daily min/max/average values and trending analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return

    # Auto-generate 7-day forecast starting today
    sel_date = date.today()
    with st.spinner("⏳ Generating 7-day forecast starting today..."):
        df_weekly, _ = generate_weekly_forecast(models, scalers, features, metadata, sel_date)
    
    st.markdown(f"<h3 style='color: #f59e0b; text-align: center;'>Week of {sel_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)
    
    # Parameter selection
    selected_target = st.selectbox("🎯 Select Parameter to Visualize", options=list(metadata.keys()), key="weekly_param")
    
    # Pre-generate hourly data for the week (used by cards and visualizations)
    hourly_dfs = []
    day_labels = []
    for d in range(7):
        current_date = sel_date + timedelta(days=d)
        day_labels.append(current_date.strftime('%Y-%m-%d'))
        df_h = generate_hourly_forecast(models, scalers, features, metadata, current_date)
        hourly_dfs.append(df_h)

    # Responsive card grid showing each day's date + average temperature
    st.markdown("""
    <style>
    .weekly-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin-bottom: 1rem;
    }
    .weekly-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    .weekly-card .day { color: #d8b4fe; font-weight: 700; margin-bottom: 6px; }
    .weekly-card .date { color: #f5f3ff; font-size: 0.95rem; margin-bottom: 8px; }
    .weekly-card .avg { font-size: 1.6rem; font-weight: 800; color: #f59e0b; }
    @media (max-width: 600px) {
        .weekly-card { padding: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

    cards_html = ['<div class="weekly-card-grid">']
    for idx, row in df_weekly.iterrows():
        try:
            day_date = date.fromisoformat(row['Date'])
        except Exception:
            # fallback: display raw
            day_date = row['Date']
        day_label = day_date.strftime('%a') if hasattr(day_date, 'strftime') else row['DayOfWeek']
        pretty_date = day_date.strftime('%b %d') if hasattr(day_date, 'strftime') else row['Date']
        avg_val = row.get(f"{selected_target}_avg", None)
        unit = metadata.get(selected_target, {}).get('unit', '')
        if avg_val is None or (isinstance(avg_val, float) and np.isnan(avg_val)):
            avg_display = '—'
        else:
            avg_display = f"{avg_val:.1f} {unit}"
        card = f'''<div class="weekly-card">
            <div class="day">{day_label}</div>
            <div class="date">{pretty_date}</div>
            <div class="avg">{avg_display}</div>
        </div>'''
        cards_html.append(card)
    cards_html.append('</div>')
    st.markdown(''.join(cards_html), unsafe_allow_html=True)

    # --- Weekly visualizations ---
    # 1) 7x24 heatmap (days x hours) for selected parameter
    try:
        hours = [f"{h:02d}:00" for h in range(24)]
        z = []
        for df_h in hourly_dfs:
            row_vals = []
            for h in hours:
                if h in df_h.columns:
                    # sometimes df_hourly stores parameter columns; prefer direct access
                    val = df_h.loc[df_h['Hour'] == h, selected_target]
                    if not val.empty:
                        row_vals.append(float(val.iloc[0]))
                    else:
                        row_vals.append(None)
                else:
                    # fallback to positional hour
                    try:
                        row_vals.append(float(df_h.iloc[int(h[:2])][selected_target]))
                    except Exception:
                        row_vals.append(None)
            z.append(row_vals)

        import plotly.graph_objects as _go
        heat = _go.Figure(data=_go.Heatmap(z=z, x=hours, y=[date.fromisoformat(d).strftime('%a %b %d') for d in day_labels], colorscale='Viridis', hoverongaps=False))
        heat.update_layout(title=f"{metadata.get(selected_target, {}).get('name', selected_target)} - Weekly Hourly Heatmap", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=360)
        st.plotly_chart(heat, use_container_width=True)
    except Exception:
        # non-fatal: skip heatmap if any error
        pass

    # 2) Min/Avg/Max bar chart for the week
    try:
        avg_vals = [row.get(f"{selected_target}_avg", None) for _, row in df_weekly.iterrows()]
        min_vals = [row.get(f"{selected_target}_min", None) for _, row in df_weekly.iterrows()]
        max_vals = [row.get(f"{selected_target}_max", None) for _, row in df_weekly.iterrows()]

        # compute asymmetric error bars
        upper_err = [ (max_vals[i] - avg_vals[i]) if (avg_vals[i] is not None and max_vals[i] is not None) else 0 for i in range(len(avg_vals)) ]
        lower_err = [ (avg_vals[i] - min_vals[i]) if (avg_vals[i] is not None and min_vals[i] is not None) else 0 for i in range(len(avg_vals)) ]

        bar_fig = _go.Figure()
        bar_fig.add_trace(_go.Bar(x=[date.fromisoformat(d).strftime('%a') for d in day_labels], y=avg_vals, name='Average', marker_color='#f59e0b', error_y=dict(type='data', symmetric=False, array=upper_err, arrayminus=lower_err)))
        bar_fig.update_layout(title=f"Weekly {metadata.get(selected_target, {}).get('name', selected_target)} - Min/Avg/Max", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=360)
        st.plotly_chart(bar_fig, use_container_width=True)
    except Exception:
        pass

    fig = create_daily_comparison_plot(df_weekly, selected_target, metadata)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key="weekly_plot_main")
    
    # FEATURE 1: Confidence Score
    st.markdown("---")
    st.markdown("### 🎯 Prediction Confidence & Quality")
    confidence = calculate_confidence_score(selected_target, df_weekly[f"{selected_target}_avg"].mean(), 
                                           df_weekly[f"{selected_target}_avg"].mean() * 0.8, 
                                           df_weekly[f"{selected_target}_avg"].std() or 1)
    display_confidence_indicator(confidence)
    
    # FEATURE 2: Historical Comparison
    st.markdown("### 📊 Comparison with Historical Data")
    display_historical_comparison(selected_target, df_weekly[f"{selected_target}_avg"].mean(), 
                                metadata[selected_target]['unit'])
    
    # FEATURE 3: Extreme Value Alerts
    st.markdown("### ⚠️ Value Range Analysis")
    max_val = df_weekly[f"{selected_target}_max"].max()
    is_extreme, alert_type = check_extreme_values(selected_target, max_val, metadata)
    display_alerts(selected_target, max_val, alert_type)
    
    # Summary table
    st.markdown("### 📊 Daily Summary Table")
    summary_display = df_weekly[['Date', 'DayOfWeek']].copy()
    for col in df_weekly.columns:
        if selected_target in col:
            summary_display[col] = df_weekly[col].round(2)
    st.dataframe(summary_display, use_container_width=True)
    
    # FEATURE 4: Quick Export Summary
    st.markdown("---")
    st.markdown("### 💾 Quick Export")
    export_summary = generate_export_summary(df_weekly, list(metadata.keys())[:5])
    create_quick_export_button(export_summary, f"weekly_forecast_{sel_date.strftime('%Y%m%d')}")
    
    # Download data
    csv = df_weekly.to_csv(index=False)
    st.download_button("📥 Download Weekly Data (CSV)", data=csv, file_name=f"weekly_forecast_{sel_date.strftime('%Y%m%d')}.csv", mime="text/csv", key="weekly_download")

    # Daily hourly details and additional visualizations
    with st.expander("📅 Daily Hourly Details & Visualizations", expanded=False):
        # Generate hourly data for each day in the week
        hourly_dfs = []
        day_labels = []
        for d in range(7):
            current_date = sel_date + timedelta(days=d)
            day_labels.append(current_date.strftime('%Y-%m-%d'))
            df_h = generate_hourly_forecast(models, scalers, features, metadata, current_date)
            hourly_dfs.append(df_h)

        # Option to show combined table
        if st.checkbox("📋 Show Combined Hourly Table", key="weekly_hourly_table"):
            combined = pd.concat([df.assign(Date=day_labels[i]) for i, df in enumerate(hourly_dfs)], ignore_index=True)
            st.dataframe(combined[['Date', 'Hour', selected_target]], use_container_width=True)

        # Per-day hourly textual list + small plot
        for i, df_day in enumerate(hourly_dfs):
            day_dt = sel_date + timedelta(days=i)
            st.markdown(f"#### {day_dt.strftime('%A, %B %d, %Y')}")
            cols = st.columns([2, 3])
            with cols[0]:
                for h in range(24):
                    hour_label = f"{h:02d}:00"
                    row = df_day[df_day['Hour'] == hour_label]
                    if not row.empty:
                        val = float(row.iloc[0][selected_target])
                        unit = metadata.get(selected_target, {}).get('unit', '')
                        display_hour = h % 12
                        if display_hour == 0:
                            display_hour = 12
                        ampm = 'AM' if h < 12 else 'PM'
                        st.markdown(f"- **{display_hour} {ampm}** — {val:.1f} {unit}")
            with cols[1]:
                fig_day = create_hourly_line_plot(df_day, metadata, selected_target, f"({day_dt.strftime('%b %d')})")
                if fig_day:
                    st.plotly_chart(fig_day, use_container_width=True, config={'displayModeBar': False})

        # Download combined hourly CSV
        combined_csv = pd.concat(hourly_dfs).to_csv(index=False)
        st.download_button("📥 Download Weekly Hourly Data (CSV)", data=combined_csv, file_name=f"weekly_hourly_{sel_date.strftime('%Y%m%d')}.csv", mime="text/csv", key="weekly_hourly_download")

# Daily Summary Page
def render_daily_summary_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">📊 Daily Summary with Max/Min</h1>
            <p class="page-subtitle">Aggregated daily predictions showing maximum, minimum, and average values</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    col1, col2 = st.columns([2, 1])
    with col1:
        sel_date = st.date_input("📅 Select Date", value=date.today(), min_value=date(2026, 1, 1), max_value=date(2035, 12, 31), key="daily_date")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🔮 Generate Daily Summary", use_container_width=True, key="daily_btn")
    
    if generate_btn:
        with st.spinner("⏳ Generating daily aggregates..."):
            df_hourly = generate_hourly_forecast(models, scalers, features, metadata, sel_date)
        
        st.markdown(f"<h3 style='color: #f59e0b; text-align: center;'>{sel_date.strftime('%A, %B %d, %Y')} - Daily Aggregates</h3>", unsafe_allow_html=True)
        
        # Create summary cards
        key_params = ['T2M', 'RH2M', 'PRECTOTCORR', 'WS10M']
        cols = st.columns(len(key_params))
        
        for i, param in enumerate(key_params):
            with cols[i]:
                meta = metadata[param]
                max_val = df_hourly[param].max()
                min_val = df_hourly[param].min()
                avg_val = df_hourly[param].mean()
                
                st.markdown(f"""
                <div class="result-card">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{meta['icon']}</div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem;">{meta['name']}</div>
                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: 700;">Max: {max_val:.{meta['decimals']}f}</div>
                    <div style="color: #06b6d4; font-size: 1.2rem; font-weight: 700;">Min: {min_val:.{meta['decimals']}f}</div>
                    <div style="color: #f59e0b; font-size: 1.2rem; font-weight: 700;">Avg: {avg_val:.{meta['decimals']}f} {meta['unit']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Full daily table
        st.markdown("### 📈 Full Daily Aggregates")
        daily_summary = pd.DataFrame()
        for param in list(metadata.keys()):
            daily_summary[f"{param}_max"] = [df_hourly[param].max()]
            daily_summary[f"{param}_min"] = [df_hourly[param].min()]
            daily_summary[f"{param}_avg"] = [df_hourly[param].mean()]
        
        st.dataframe(daily_summary.round(3), use_container_width=True)

    # Monthly Forecast Page (30 days)
    def render_monthly_page():
        render_back_button()

        st.markdown("""
        <div class="prediction-page">
            <div class="page-header">
                <h1 class="page-title">📆 30-Day Monthly Forecast</h1>
                <p class="page-subtitle">Monthly forecast with daily min/max/average values and trend visualizations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not models_loaded:
            st.error("⚠️ Models not loaded. Please run: python train_models.py")
            return

        sel_date = date.today()
        with st.spinner("⏳ Generating 30-day forecast starting today..."):
            df_monthly = generate_monthly_forecast(models, scalers, features, metadata, sel_date)

        st.markdown(f"<h3 style='color: #f59e0b; text-align: center;'>Month starting {sel_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)

        # Parameter selection
        selected_target = st.selectbox("🎯 Select Parameter to Visualize", options=list(metadata.keys()), key="monthly_param")

        # Summary cards grid (responsive) showing date and average
        st.markdown("""
        <style>
        .monthly-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 12px 0; }
        .monthly-card { background: rgba(255,255,255,0.04); padding: 10px; border-radius: 8px; text-align:center; border:1px solid rgba(255,255,255,0.04); }
        .monthly-card .day { color: #d8b4fe; font-weight:700; }
        .monthly-card .date { color: #f5f3ff; font-size:0.85rem; }
        .monthly-card .avg { color: #f59e0b; font-weight:800; font-size:1.1rem; }
        </style>
        """, unsafe_allow_html=True)

        cards = ['<div class="monthly-grid">']
        for _, r in df_monthly.iterrows():
            try:
                d = date.fromisoformat(r['Date'])
                day_label = d.strftime('%a')
                pretty = d.strftime('%b %d')
            except Exception:
                day_label = r.get('DayOfWeek', '')
                pretty = r.get('Date', '')
            avg = r.get(f"{selected_target}_avg", None)
            unit = metadata.get(selected_target, {}).get('unit', '')
            avg_text = '—' if avg is None or (isinstance(avg, float) and np.isnan(avg)) else f"{avg:.1f} {unit}"
            cards.append(f"<div class='monthly-card'><div class='day'>{day_label}</div><div class='date'>{pretty}</div><div class='avg'>{avg_text}</div></div>")
        cards.append('</div>')
        st.markdown(''.join(cards), unsafe_allow_html=True)

        # Main trend visualization (min/avg/max over 30 days)
        try:
            fig = create_daily_comparison_plot(df_monthly, selected_target, metadata)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key='monthly_main')
        except Exception:
            st.warning('Could not render main trend plot for monthly forecast.')

        # Min/Avg/Max bar chart for month
        try:
            import plotly.graph_objects as _go
            days = [date.fromisoformat(d).strftime('%d') if isinstance(d, str) else d.strftime('%d') for d in df_monthly['Date']]
            avg_vals = df_monthly[f"{selected_target}_avg"].tolist()
            min_vals = df_monthly[f"{selected_target}_min"].tolist()
            max_vals = df_monthly[f"{selected_target}_max"].tolist()
            upper = [max_vals[i]-avg_vals[i] for i in range(len(avg_vals))]
            lower = [avg_vals[i]-min_vals[i] for i in range(len(avg_vals))]
            bar = _go.Figure()
            bar.add_trace(_go.Bar(x=days, y=avg_vals, name='Average', marker_color='#f59e0b', error_y=dict(type='data', symmetric=False, array=upper, arrayminus=lower)))
            bar.update_layout(title=f"Monthly {metadata.get(selected_target, {}).get('name', selected_target)} - Min/Avg/Max", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420)
            st.plotly_chart(bar, use_container_width=True)
        except Exception:
            pass

        # Download and quick export
        st.markdown('---')
        st.markdown('### 💾 Quick Export')
        export_summary = generate_export_summary(df_monthly, list(metadata.keys())[:5])
        create_quick_export_button(export_summary, f"monthly_forecast_{sel_date.strftime('%Y%m%d')}")
        csv = df_monthly.to_csv(index=False)
        st.download_button("📥 Download Monthly Data (CSV)", data=csv, file_name=f"monthly_forecast_{sel_date.strftime('%Y%m%d')}.csv", mime='text/csv', key='monthly_download')


    # 12-Month Forecast Page (Yearly overview by month)
    def render_12month_page():
        render_back_button()

        st.markdown("""
        <div class="prediction-page">
            <div class="page-header">
                <h1 class="page-title">📈 12-Month Forecast</h1>
                <p class="page-subtitle">Monthly aggregates for the next 12 months with trend visualizations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not models_loaded:
            st.error("⚠️ Models not loaded. Please run: python train_models.py")
            return

        sel_date = date.today()
        # start from first day of current month
        start_month = date(sel_date.year, sel_date.month, 1)

        def add_months(d, months):
            # d is a date object (from injected `date`), months is int
            year = d.year + (d.month - 1 + months) // 12
            month = (d.month - 1 + months) % 12 + 1
            day = min(d.day, (date(year, month % 12 + 1, 1) - timedelta(days=1)).day)
            return date(year, month, day)

        selected_target = st.selectbox("🎯 Select Parameter to Visualize (12 months)", options=list(metadata.keys()), index=0, key="12m_param")

        month_labels = []
        monthly_min = []
        monthly_avg = []
        monthly_max = []
        monthly_dfs = []

        for m in range(12):
            ms = add_months(start_month, m)
            month_labels.append(ms.strftime('%b %Y'))
            # generate 30-day forecast starting at first of month and aggregate
            df_days = generate_monthly_forecast(models, scalers, features, metadata, ms)
            monthly_dfs.append(df_days)
            monthly_min.append(df_days[f"{selected_target}_min"].min())
            monthly_avg.append(df_days[f"{selected_target}_avg"].mean())
            monthly_max.append(df_days[f"{selected_target}_max"].max())

        # Cards grid for 12 months
        st.markdown("""
        <style>
        .ygrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin: 12px 0; }
        .ycard { background: rgba(255,255,255,0.04); padding: 12px; border-radius: 8px; text-align:center; border:1px solid rgba(255,255,255,0.04); }
        .ycard .month { color: #d8b4fe; font-weight:700; }
        .ycard .avg { color: #f59e0b; font-weight:800; font-size:1.2rem; }
        </style>
        """, unsafe_allow_html=True)

        cards_html = ['<div class="ygrid">']
        for i in range(12):
            avg = monthly_avg[i]
            unit = metadata.get(selected_target, {}).get('unit', '')
            avg_text = '—' if avg is None or (isinstance(avg, float) and np.isnan(avg)) else f"{avg:.1f} {unit}"
            cards_html.append(f"<div class='ycard'><div class='month'>{month_labels[i]}</div><div class='avg'>{avg_text}</div></div>")
        cards_html.append('</div>')
        st.markdown(''.join(cards_html), unsafe_allow_html=True)

        # Trend line for avg over 12 months
        try:
            import plotly.graph_objects as _go
            fig = _go.Figure()
            fig.add_trace(_go.Scatter(x=month_labels, y=monthly_avg, mode='lines+markers', name='Avg', line=dict(color='#f59e0b')))
            fig.add_trace(_go.Scatter(x=month_labels, y=monthly_min, mode='lines+markers', name='Min', line=dict(color='#06b6d4')))
            fig.add_trace(_go.Scatter(x=month_labels, y=monthly_max, mode='lines+markers', name='Max', line=dict(color='#ef4444')))
            fig.update_layout(title=f"12-Month {metadata.get(selected_target, {}).get('name', selected_target)} Trend", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning('Could not render 12-month trend plot.')

        # Bar chart with error bars
        try:
            bar = _go.Figure()
            upper = [monthly_max[i]-monthly_avg[i] for i in range(12)]
            lower = [monthly_avg[i]-monthly_min[i] for i in range(12)]
            bar.add_trace(_go.Bar(x=month_labels, y=monthly_avg, name='Average', marker_color='#f59e0b', error_y=dict(type='data', symmetric=False, array=upper, arrayminus=lower)))
            bar.update_layout(title='Monthly Average with Min/Max Error Bars', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420)
            st.plotly_chart(bar, use_container_width=True)
        except Exception:
            pass

        # Quick export and download aggregated monthly CSV
        agg_df = pd.DataFrame({'Month': month_labels, f"{selected_target}_min": monthly_min, f"{selected_target}_avg": monthly_avg, f"{selected_target}_max": monthly_max})
        st.markdown('---')
        st.markdown('### 💾 Quick Export')
        export_summary = generate_export_summary(agg_df, [f"{selected_target}_avg", f"{selected_target}_min", f"{selected_target}_max"]) 
        create_quick_export_button(export_summary, f"12month_forecast_{sel_date.strftime('%Y%m%d')}")
        st.download_button("📥 Download 12-Month Aggregates (CSV)", data=agg_df.to_csv(index=False), file_name=f"12month_{sel_date.strftime('%Y%m%d')}.csv", mime='text/csv', key='12m_download')
# Research Export Page
def render_research_page():
    render_back_button()
    
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">📑 Research Paper Export</h1>
            <p class="page-subtitle">Export model metrics, statistics, and forecasts for academic publications</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return
    
    st.markdown("### 🤖 Model Performance Metrics")
    
    # Load model results
    model_results = joblib.load('models/model_results.pkl')
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_r2 = np.mean([m['R2'] for m in model_results.values()])
    avg_mae = np.mean([m['MAE'] for m in model_results.values()])
    avg_rmse = np.mean([m['RMSE'] for m in model_results.values()])
    max_r2 = max([m['R2'] for m in model_results.values()])
    
    with col1:
        st.markdown(f"""<div class="result-card"><div class="stat-number">{avg_r2:.4f}</div><div class="stat-label">Avg R² Score</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="result-card"><div class="stat-number">{max_r2:.4f}</div><div class="stat-label">Best R² Score</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="result-card"><div class="stat-number">{avg_mae:.4f}</div><div class="stat-label">Avg MAE</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="result-card"><div class="stat-number">{avg_rmse:.4f}</div><div class="stat-label">Avg RMSE</div></div>""", unsafe_allow_html=True)
    
    # Detailed metrics table
    st.markdown("### 📊 Detailed Model Metrics by Parameter")
    metrics_df = pd.DataFrame.from_dict(model_results, orient='index')
    metrics_df = metrics_df.round(4)
    st.dataframe(metrics_df, use_container_width=True)
    
    # Export options
    st.markdown("### 📥 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export Metrics as JSON", use_container_width=True, key="export_json"):
            export_json = json.dumps({
                'export_date': datetime.now().isoformat(),
                'institution': 'Mohan Babu University, Tirupati',
                'avg_r2': float(avg_r2),
                'avg_mae': float(avg_mae),
                'avg_rmse': float(avg_rmse),
                'model_count': len(model_results),
                'metrics': {k: {kk: float(vv) for kk, vv in v.items()} for k, v in model_results.items()}
            }, indent=2)
            
            st.download_button("📥 Download Metrics JSON", data=export_json, file_name=f"model_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json", key="dl_json")
    
    with col2:
        if st.button("📊 Export Metrics as CSV", use_container_width=True, key="export_csv"):
            csv_data = metrics_df.to_csv()
            st.download_button("📥 Download Metrics CSV", data=csv_data, file_name=f"model_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv", key="dl_csv")
    
    # Generate research report
    st.markdown("### 📝 Research Report")
    if st.button("📑 Generate Research Report", use_container_width=True, key="gen_report"):
        report_data = {
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'institution': 'Mohan Babu University, Tirupati',
            'metrics': model_results
        }
        report = generate_research_report(report_data, metadata)
        
        st.markdown(report)
        
        st.download_button(
            "📥 Download Research Report (.txt)",
            data=report,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="dl_report"
        )


def render_10day_page():
    render_back_button()
    st.markdown("""
    <div class="prediction-page">
        <div class="page-header">
            <h1 class="page-title">📆 10-Day Forecast</h1>
            <p class="page-subtitle">Extended 10-day forecast with daily min/max/average and trend analysis</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not models_loaded:
        st.error("⚠️ Models not loaded. Please run: python train_models.py")
        return

    sel_date = date.today()
    with st.spinner("⏳ Generating 10-day forecast starting today..."):
        df_10day, _ = generate_10day_forecast(models, scalers, features, metadata, sel_date)

    st.markdown(f"<h3 style='color: #f59e0b; text-align: center;'>10-Day Forecast starting {sel_date.strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)

    default_param = 'T2M' if 'T2M' in metadata else list(metadata.keys())[0]
    fig = create_daily_comparison_plot(df_10day, default_param, metadata)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}, key="10day_plot_main")

    with st.expander("Options: change parameter or export data", expanded=False):
        selected_target = st.selectbox("🎯 Select Parameter to Visualize", options=list(metadata.keys()), index=list(metadata.keys()).index(default_param), key="10day_param")
        fig2 = create_daily_comparison_plot(df_10day, selected_target, metadata)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': True}, key="10day_plot_selected")

        st.markdown("---")
        st.markdown("### 📊 10-Day Summary Table")
        display_cols = ['Date', 'DayOfWeek'] + [c for c in df_10day.columns if selected_target in c]
        st.dataframe(df_10day[display_cols].round(2), use_container_width=True)

        st.markdown("---")
        export_summary = generate_export_summary(df_10day, list(metadata.keys())[:5])
        create_quick_export_button(export_summary, f"10day_forecast_{sel_date.strftime('%Y%m%d')}")

        csv = df_10day.to_csv(index=False)
        st.download_button("📥 Download 10-Day Data (CSV)", data=csv, file_name=f"10day_forecast_{sel_date.strftime('%Y%m%d')}.csv", mime="text/csv", key="10day_download")
