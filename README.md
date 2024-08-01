# OpenDevin-MultiAgent-Workflows

A summary of the below references can be found at
https://www.overleaf.com/read/bsvdkyxwdxrr#89bfbb

# Roles Comparison

| Work          | Analysis & Design                     | Implementation                  | Review                                     | Testing                         | Deployment                         |
| ---------     | ------------------------------------- | ------------------------------- | ------------------------------------------ | ------------------------------- | ---------------------------------- |
| `Chatdev`     | Design                                | CodingWriting & CodeCompleteAll | CodeReviewComment & CodeReviewModification | TestErrorSummary & TestErrorFix | EnviromentSetupDoc & ManualWriting |
| `magis`       | manager                                   | developer                          | qa_engineer                                        | qa_engineer      | ....
| `CodeR`       | Manager.create_plan                   | Editor                          | FaultLocalizer                             | Verifier                        | Manager.interpret_execution_summary|
| `CoAct`       | GlobalPlanningAgent                   | LocalExecutionAgent             | GlobalPlanningAgent                        | LocalExecutionAgent             | GlobalPlanningAgent
| `aide`        | understand_symbol & provide_insights  | propose change                  | ...                                        | run_tests & gather_feedback     | DeveloperInLoop                    |
| `devOpsGPT`   | analyze_requirements, clarify_requirements, define_api, split_tasks     | generate_code  | auto_self_check     | unit_testing, integration_testing, deployment_testing |  check_working_software
| `meta_GPT`    | product_manager, architect, project_manager | engineer                          | qa_engineer                                        |qa_engineer      | project_manager
| `patchflows`  | ...                                   | ...                          | ...                                        |

# References

- D. Chen, S. Lin, M. Zeng, D. Zan, J.-G. Wang, A. Cheshkov, J. Sun, H. Yu, G. Dong, A. Aliev, J. Wang, X. Cheng, G. Liang, Y. Ma, P. Bian, T. Xie, and Q. Wang, “CodeR: Issue Resolving with Multi-Agent and Task Graphs,” 2024, publisher: arXiv Version Number: 3. [Online]. Available: https://arxiv.org/abs/2406.01304

- W. Tao, Y. Zhou, W. Zhang, and Y.-X. Cheng, “MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution,” arXiv.org, 2024. [Online]. Available: https://arxiv.org/abs/2403.17927

- S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, “MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework,” 2023, publisher: arXiv Version Number: 5. [Online]. Available: https://arxiv.org/abs/2308.00352

- X. Hou, M. Yang, W. Jiao, X. Wang, Z. Tu, and W. X. Zhao, “CoAct: A Global-Local Hierarchy for Autonomous Agent Collaboration,” June 2024, arXiv:2406.13381 [cs]. [Online]. Available: http://arxiv.org/abs/2406.13381

- DevOpsGPT: AI-Driven Software Development Automation Solution. [Online]. Available: https://github.com/kuafuai/DevOpsGPT

- Patched: Open Source AI workflows for software development. [Online]. Available: https://www.patched.codes

- Aide’s SOTA multi-agent coding framework. [Online]. Available: https://aide.dev/blog/sota-on-swe-bench-lite

- Chatdev: Communicative agents for software development. [Online]. Available: https://arxiv.org/abs/2307.07924. GitHub: https://github.com/OpenBMB/ChatDev
