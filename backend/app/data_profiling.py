"""
Module: Data Quality Profiling

Comprehensive dataset analysis before training
- Missing values analysis
- Outlier detection
- Class imbalance
- Feature correlation
- Data types and distributions
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from typing import Dict, List, Any, Tuple


def profile_dataset(df: pd.DataFrame, target_column: str = None, task_type: str = 'classification') -> Dict[str, Any]:
    """
    Generate comprehensive dataset profile.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset
    target_column : str, optional
        Name of target column for class analysis
    task_type : str
        'classification' or 'regression'
    
    Returns:
    --------
    dict : Complete dataset profile
    """
    
    print(f"\n🔍 Data Quality Profile:")
    print(f"   Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    profile = {
        'shape': {'rows': df.shape[0], 'columns': df.shape[1]},
        'columns': {},
        'missing_values': {},
        'data_types': {},
        'correlations': None,
        'class_distribution': None,
        'quality_score': 0.0,
        'issues': []
    }
    
    # 1. Column-level analysis
    print(f"\n   📋 Column Analysis:")
    for col in df.columns:
        col_data = df[col]
        col_type = col_data.dtype
        
        missing_pct = (col_data.isnull().sum() / len(col_data)) * 100
        unique_count = col_data.nunique()
        
        col_profile = {
            'dtype': str(col_type),
            'null_count': int(col_data.isnull().sum()),
            'null_percentage': float(missing_pct),
            'unique_values': int(unique_count),
            'unique_percentage': float((unique_count / len(col_data)) * 100)
        }
        
        # Numeric analysis
        if np.issubdtype(col_type, np.number):
            col_profile.update({
                'mean': float(col_data.mean()) if col_data.notna().any() else None,
                'median': float(col_data.median()) if col_data.notna().any() else None,
                'std': float(col_data.std()) if col_data.notna().any() else None,
                'min': float(col_data.min()) if col_data.notna().any() else None,
                'max': float(col_data.max()) if col_data.notna().any() else None,
                'skewness': float(skew(col_data.dropna())) if len(col_data.dropna()) > 0 else None,
                'kurtosis': float(kurtosis(col_data.dropna())) if len(col_data.dropna()) > 0 else None,
            })
        else:
            # Categorical analysis
            top_values = col_data.value_counts().head(5)
            col_profile['top_values'] = top_values.to_dict()
        
        profile['columns'][col] = col_profile
        profile['missing_values'][col] = float(missing_pct)
        profile['data_types'][col] = str(col_type)
        
        if missing_pct > 0:
            print(f"      ⚠️  {col}: {missing_pct:.1f}% missing ({col_data.isnull().sum()} values)")
    
    # 2. Missing values quality score
    total_missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100
    missing_quality = max(0, 100 - total_missing_pct * 2)
    
    if total_missing_pct > 20:
        profile['issues'].append('⚠️  High missing data (>20%) - consider imputation or removal')
    
    # 3. Outlier detection (IQR method)
    print(f"\n   🔎 Outlier Detection:")
    outlier_counts = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
        outlier_pct = (outliers / len(df)) * 100
        outlier_counts[col] = {'outliers': int(outliers), 'percentage': float(outlier_pct)}
        
        if outlier_pct > 5:
            print(f"      ⚠️  {col}: {outlier_pct:.1f}% outliers detected")
            profile['issues'].append(f"⚠️  {col} has {outlier_pct:.1f}% outliers")
    
    profile['outliers'] = outlier_counts
    outlier_quality = 100 - max(0, sum(v['percentage'] for v in outlier_counts.values()) / len(outlier_counts))
    
    # 4. Class distribution (classification)
    if target_column and target_column in df.columns:
        print(f"\n   🎯 Class Distribution:")
        class_dist = df[target_column].value_counts()
        class_total = len(df)
        
        class_dist_pct = (class_dist / class_total * 100).to_dict()
        profile['class_distribution'] = {
            'classes': class_dist.to_dict(),
            'percentages': class_dist_pct,
            'imbalance_ratio': float(class_dist.max() / class_dist.min()) if len(class_dist) > 1 else 1.0
        }
        
        imbalance_ratio = profile['class_distribution']['imbalance_ratio']
        print(f"      📊 Imbalance Ratio: {imbalance_ratio:.2f}:1")
        
        for cls, pct in class_dist_pct.items():
            print(f"         Class {cls}: {pct:.1f}%")
        
        if imbalance_ratio > 3:
            profile['issues'].append(f"⚠️  Class imbalance detected ({imbalance_ratio:.1f}:1) - consider SMOTE or class weights")
    
    # 5. Feature correlations
    print(f"\n   🔗 Feature Correlations:")
    numeric_df = df.select_dtypes(include=[np.number])
    
    if len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr()
        # Find highly correlated pairs (>0.9)
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.9:
                    high_corr_pairs.append({
                        'feature_1': corr_matrix.columns[i],
                        'feature_2': corr_matrix.columns[j],
                        'correlation': float(corr_value)
                    })
        
        profile['correlations'] = {
            'high_correlation_pairs': high_corr_pairs,
            'matrix': corr_matrix.values.tolist()
        }
        
        if high_corr_pairs:
            print(f"      ⚠️  Found {len(high_corr_pairs)} highly correlated feature pairs (>0.9)")
            profile['issues'].append(f"⚠️  {len(high_corr_pairs)} highly correlated features - consider dropping one")
    
    # 6. Overall quality score
    duplicate_rows = df.duplicated().sum()
    duplicate_quality = 100 - (duplicate_rows / len(df)) * 100
    
    if duplicate_rows > 0:
        profile['issues'].append(f"⚠️  {duplicate_rows} duplicate rows detected")
        print(f"\n   ⚠️  Duplicate Rows: {duplicate_rows}")
    
    # Weighted average quality score
    profile['quality_score'] = float((missing_quality + outlier_quality + duplicate_quality) / 3)
    
    print(f"\n   📈 Data Quality Score: {profile['quality_score']:.1f}/100")
    print(f"   ⏰ Issues Found: {len(profile['issues'])}")
    
    return profile


def get_data_quality_recommendations(profile: Dict[str, Any]) -> List[str]:
    """
    Generate actionable recommendations based on data profile.
    
    Parameters:
    -----------
    profile : dict
        Output from profile_dataset()
    
    Returns:
    --------
    list : Recommendations
    """
    
    recommendations = profile['issues'].copy()
    
    if profile['quality_score'] < 70:
        recommendations.insert(0, "🔴 Data quality is low. Recommend significant preprocessing.")
    elif profile['quality_score'] < 85:
        recommendations.insert(0, "🟡 Data quality is moderate. Review preprocessing options.")
    else:
        recommendations.insert(0, "🟢 Data quality is good. Ready for model training.")
    
    return recommendations


def generate_data_quality_summary(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate concise quality summary.
    
    Parameters:
    -----------
    profile : dict
        Output from profile_dataset()
    
    Returns:
    --------
    dict : Quality summary
    """
    
    missing_cols = [k for k, v in profile['missing_values'].items() if v > 0]
    outlier_cols = [k for k, v in profile['outliers'].items() if v['percentage'] > 5]
    
    return {
        'overall_quality': profile['quality_score'],
        'missing_data_percentage': sum(profile['missing_values'].values()) / len(profile['missing_values']),
        'columns_with_missing': len(missing_cols),
        'columns_with_outliers': len(outlier_cols),
        'total_issues': len(profile['issues']),
        'quality_grade': (
            'A' if profile['quality_score'] >= 90 else
            'B' if profile['quality_score'] >= 80 else
            'C' if profile['quality_score'] >= 70 else
            'D' if profile['quality_score'] >= 60 else
            'F'
        ),
        'recommendation': profile['issues'][0] if profile['issues'] else "Data quality is excellent"
    }
