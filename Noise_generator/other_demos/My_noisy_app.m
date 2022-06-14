classdef My_noisy_app < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        MortgageCalculatorUIFigure     matlab.ui.Figure
        GridLayout                     matlab.ui.container.GridLayout
        LeftPanel                      matlab.ui.container.Panel
        MonthlyPaymentEditField        matlab.ui.control.NumericEditField
        MonthlyPaymentButton           matlab.ui.control.Button
        LoanPeriodYearsEditField       matlab.ui.control.NumericEditField
        LoanPeriodYearsEditFieldLabel  matlab.ui.control.Label
        InterestRateEditField          matlab.ui.control.NumericEditField
        InterestRateEditFieldLabel     matlab.ui.control.Label
        LoanAmountEditField            matlab.ui.control.NumericEditField
        LoanAmountEditFieldLabel       matlab.ui.control.Label
        RightPanel                     matlab.ui.container.Panel
        PrincipalInterestUIAxes        matlab.ui.control.UIAxes
    end

    % Properties that correspond to apps with auto-reflow
    properties (Access = private)
        onePanelWidth = 576;
    end

    % Callbacks that handle component events
    methods (Access = private)

        % Changes arrangement of the app based on UIFigure width
        function updateAppLayout(app, event)
            currentFigureWidth = app.MortgageCalculatorUIFigure.Position(3);
            if(currentFigureWidth <= app.onePanelWidth)
                % Change to a 2x1 grid
                app.GridLayout.RowHeight = {316, 316};
                app.GridLayout.ColumnWidth = {'1x'};
                app.RightPanel.Layout.Row = 2;
                app.RightPanel.Layout.Column = 1;
            else
                % Change to a 1x2 grid
                app.GridLayout.RowHeight = {'1x'};
                app.GridLayout.ColumnWidth = {257, '1x'};
                app.RightPanel.Layout.Row = 1;
                app.RightPanel.Layout.Column = 2;
            end
        end

        % Button pushed function: MonthlyPaymentButton
        function MonthlyPaymentButtonPushed(app, event)
                       
            % Calculate the monthly payment
            amount = app.LoanAmountEditField.Value;
            rate = app.InterestRateEditField.Value/12/100;
            nper = 12*app.LoanPeriodYearsEditField.Value;
            payment = (amount*rate)/(1-(1+rate)^-nper);
            app.MonthlyPaymentEditField.Value = payment;
            
            % pre allocating and initializing variables
            interest = zeros(1,nper);
            principal = zeros(1,nper);
            balance = zeros (1,nper);
            
            balance(1) = amount;
            
            % Calculate the principal and interest over time
            for i = 1:nper
                interest(i)  = balance(i)*rate;
                principal(i) = payment - interest(i);
                balance(i+1) = balance(i) - principal(i);
            end
            
            % Plot the principal and interest
            plot(app.PrincipalInterestUIAxes,(1:nper)',principal, ...
                (1:nper)',interest);
            legend(app.PrincipalInterestUIAxes,{'Principal','Interest'},'Location','Best')
            xlim(app.PrincipalInterestUIAxes,[0 nper]); 
            
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create MortgageCalculatorUIFigure and hide until all components are created
            app.MortgageCalculatorUIFigure = uifigure('Visible', 'off');
            app.MortgageCalculatorUIFigure.AutoResizeChildren = 'off';
            app.MortgageCalculatorUIFigure.Position = [100 100 653 316];
            app.MortgageCalculatorUIFigure.Name = 'Mortgage Calculator';
            app.MortgageCalculatorUIFigure.SizeChangedFcn = createCallbackFcn(app, @updateAppLayout, true);

            % Create GridLayout
            app.GridLayout = uigridlayout(app.MortgageCalculatorUIFigure);
            app.GridLayout.ColumnWidth = {257, '1x'};
            app.GridLayout.RowHeight = {'1x'};
            app.GridLayout.ColumnSpacing = 0;
            app.GridLayout.RowSpacing = 0;
            app.GridLayout.Padding = [0 0 0 0];
            app.GridLayout.Scrollable = 'on';

            % Create LeftPanel
            app.LeftPanel = uipanel(app.GridLayout);
            app.LeftPanel.Layout.Row = 1;
            app.LeftPanel.Layout.Column = 1;
            app.LeftPanel.Scrollable = 'on';

            % Create LoanAmountEditFieldLabel
            app.LoanAmountEditFieldLabel = uilabel(app.LeftPanel);
            app.LoanAmountEditFieldLabel.HorizontalAlignment = 'right';
            app.LoanAmountEditFieldLabel.Position = [50 230 77 22];
            app.LoanAmountEditFieldLabel.Text = 'Loan Amount';

            % Create LoanAmountEditField
            app.LoanAmountEditField = uieditfield(app.LeftPanel, 'numeric');
            app.LoanAmountEditField.Limits = [0 10000000];
            app.LoanAmountEditField.ValueDisplayFormat = '%8.f';
            app.LoanAmountEditField.Position = [142 230 100 22];
            app.LoanAmountEditField.Value = 300000;

            % Create InterestRateEditFieldLabel
            app.InterestRateEditFieldLabel = uilabel(app.LeftPanel);
            app.InterestRateEditFieldLabel.HorizontalAlignment = 'right';
            app.InterestRateEditFieldLabel.Position = [39 177 88 22];
            app.InterestRateEditFieldLabel.Text = 'Interest Rate %';

            % Create InterestRateEditField
            app.InterestRateEditField = uieditfield(app.LeftPanel, 'numeric');
            app.InterestRateEditField.Limits = [0.001 100];
            app.InterestRateEditField.Position = [142 177 100 22];
            app.InterestRateEditField.Value = 4;

            % Create LoanPeriodYearsEditFieldLabel
            app.LoanPeriodYearsEditFieldLabel = uilabel(app.LeftPanel);
            app.LoanPeriodYearsEditFieldLabel.HorizontalAlignment = 'right';
            app.LoanPeriodYearsEditFieldLabel.Position = [15 124 112 22];
            app.LoanPeriodYearsEditFieldLabel.Text = 'Loan Period (Years)';

            % Create LoanPeriodYearsEditField
            app.LoanPeriodYearsEditField = uieditfield(app.LeftPanel, 'numeric');
            app.LoanPeriodYearsEditField.Limits = [10 40];
            app.LoanPeriodYearsEditField.ValueDisplayFormat = '%.0f';
            app.LoanPeriodYearsEditField.Position = [142 124 100 22];
            app.LoanPeriodYearsEditField.Value = 30;

            % Create MonthlyPaymentButton
            app.MonthlyPaymentButton = uibutton(app.LeftPanel, 'push');
            app.MonthlyPaymentButton.ButtonPushedFcn = createCallbackFcn(app, @MonthlyPaymentButtonPushed, true);
            app.MonthlyPaymentButton.Position = [19 71 108 22];
            app.MonthlyPaymentButton.Text = 'Monthly Payment';

            % Create MonthlyPaymentEditField
            app.MonthlyPaymentEditField = uieditfield(app.LeftPanel, 'numeric');
            app.MonthlyPaymentEditField.ValueDisplayFormat = '%7.2f';
            app.MonthlyPaymentEditField.Editable = 'off';
            app.MonthlyPaymentEditField.Position = [142 71 100 22];

            % Create RightPanel
            app.RightPanel = uipanel(app.GridLayout);
            app.RightPanel.Layout.Row = 1;
            app.RightPanel.Layout.Column = 2;
            app.RightPanel.Scrollable = 'on';

            % Create PrincipalInterestUIAxes
            app.PrincipalInterestUIAxes = uiaxes(app.RightPanel);
            title(app.PrincipalInterestUIAxes, 'Principal and Interest')
            xlabel(app.PrincipalInterestUIAxes, 'Time (Months)')
            ylabel(app.PrincipalInterestUIAxes, 'Amount')
            app.PrincipalInterestUIAxes.Position = [30 36 326 250];

            % Show the figure after all components are created
            app.MortgageCalculatorUIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = My_noisy_app

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.MortgageCalculatorUIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.MortgageCalculatorUIFigure)
        end
    end
end