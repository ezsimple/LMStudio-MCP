#!/usr/bin/env python3
# lmstudio_combined.py - Integration module for lmstudio_bridge and extensions

# 두 모듈을 모두 임포트합니다
import lmstudio_bridge
import lmstudio_bridge_enhanced

# 필요한 함수나 객체를 직접 노출시킬 수 있습니다
from lmstudio_bridge import (
    mcp, LMSTUDIO_API_BASE, DEFAULT_MODEL,
    log_error, log_info,
    health_check, list_models, get_current_model, chat_completion
)

from lmstudio_bridge_enhanced import (
    enhanced_chat_completion, batch_chat_completion
    # ... 기타 확장 함수들
)

def main():
    """Entry point for the combined LM Studio Bridge MCP Server"""
    log_info("Starting Combined LM Studio Bridge MCP Server")
    log_info("Basic and enhanced features are available")
    # lmstudio_bridge의 MCP 인스턴스를 사용합니다
    lmstudio_bridge.mcp.run()

if __name__ == "__main__":
    # 통합 서버 실행
    main()