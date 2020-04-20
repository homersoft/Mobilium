//
//  AppCoordinator.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import UIKit

class AppCoordinator: LoginViewCoordinator, AccountCoordinator {
    private let window: UIWindow
    private let userRepository: CurrentUserRepository
    private let moduleFactory: ModuleFactory
    private lazy var navigationController = UINavigationController()

    init(window: UIWindow,
         moduleFactory: ModuleFactory = .init(),
         userRepository: CurrentUserRepository = .init()) {
        self.window = window
        self.moduleFactory = moduleFactory
        self.userRepository = userRepository
    }

    func navigateToInitialView() {
        window.rootViewController = navigationController
        switch userRepository.getCurrentUser() {
        case let user?:
            showAccountInfo(for: user)
        case .none:
            showLoginView()
        }
    }

    func showAccountInfo(for user: User) {
        let vc = moduleFactory.makeAccountVC(for: user, coordinator: self)
        navigationController.setViewControllers([vc], animated: true)
    }

    func showLoginView() {
        let vc = moduleFactory.makeLoginVC(coordinator: self)
        navigationController.setViewControllers([vc], animated: true)
    }
}
